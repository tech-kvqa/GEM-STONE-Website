from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_
from typing import List, Optional, Any, Dict
from app.core.database import get_db
from app.core.security import get_current_user, require_user
from app.models.user import Product, ProductImage, Review, Category
from app.schemas.schemas import ProductSummary, ProductDetail, ProductCreate, ProductUpdate

router = APIRouter()

def get_rating_stats(db: Session, product_id: int):
    stats = db.query(
        func.avg(Review.rating).label("avg"),
        func.count(Review.id).label("cnt")
    ).filter(Review.product_id == product_id).first()
    return {
        "avg_rating": round(float(stats.avg), 1) if stats.avg else None,
        "review_count": stats.cnt or 0
    }

def product_to_dict(p: Product, db: Session) -> dict:
    """Convert ORM product to plain dict with rating stats so Pydantic can serialize it."""
    stats = get_rating_stats(db, p.id)
    return {
        "id": p.id,
        "name": p.name,
        "slug": p.slug,
        "sku": p.sku,
        "price": p.price,
        "compare_price": p.compare_price,
        "stock_qty": p.stock_qty,
        "is_featured": p.is_featured,
        "is_bestseller": p.is_bestseller,
        "is_new_arrival": p.is_new_arrival,
        "description": p.description,
        "story": p.story,
        "healing_props": p.healing_props,
        "chakra": p.chakra,
        "zodiac": p.zodiac,
        "origin": p.origin,
        "weight_grams": p.weight_grams,
        "dimensions": p.dimensions,
        "category": {
            "id": p.category.id,
            "name": p.category.name,
            "slug": p.category.slug,
            "description": p.category.description,
            "story": p.category.story,
            "image_url": p.category.image_url,
            "banner_url": p.category.banner_url,
            "sort_order": p.category.sort_order,
        } if p.category else None,
        "images": [
            {
                "id": img.id,
                "url": img.url,
                "alt_text": img.alt_text,
                "is_primary": img.is_primary,
                "sort_order": img.sort_order,
            }
            for img in p.images
        ],
        "avg_rating": stats["avg_rating"],
        "review_count": stats["review_count"],
    }


@router.get("/featured")
def get_featured(db: Session = Depends(get_db)):
    products = db.query(Product).options(
        joinedload(Product.images), joinedload(Product.category)
    ).filter(Product.is_active == True, Product.is_featured == True).limit(8).all()
    return [product_to_dict(p, db) for p in products]


@router.get("/bestsellers")
def get_bestsellers(db: Session = Depends(get_db)):
    products = db.query(Product).options(
        joinedload(Product.images), joinedload(Product.category)
    ).filter(Product.is_active == True, Product.is_bestseller == True).limit(8).all()
    return [product_to_dict(p, db) for p in products]


@router.get("/new-arrivals")
def get_new_arrivals(db: Session = Depends(get_db)):
    products = db.query(Product).options(
        joinedload(Product.images), joinedload(Product.category)
    ).filter(Product.is_active == True, Product.is_new_arrival == True).limit(8).all()
    return [product_to_dict(p, db) for p in products]


@router.get("/")
def list_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = "created_at_desc",
    featured: Optional[bool] = None,
    bestseller: Optional[bool] = None,
    new_arrival: Optional[bool] = None,
    chakra: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product).options(
        joinedload(Product.images),
        joinedload(Product.category)
    ).filter(Product.is_active == True)

    if category:
        query = query.join(Category).filter(Category.slug == category)
    if search:
        query = query.filter(or_(
            Product.name.ilike(f"%{search}%"),
            Product.description.ilike(f"%{search}%"),
            Product.chakra.ilike(f"%{search}%"),
        ))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if featured is not None:
        query = query.filter(Product.is_featured == featured)
    if bestseller is not None:
        query = query.filter(Product.is_bestseller == bestseller)
    if new_arrival is not None:
        query = query.filter(Product.is_new_arrival == new_arrival)
    if chakra:
        query = query.filter(Product.chakra.ilike(f"%{chakra}%"))

    sort_map = {
        "price_asc":       Product.price.asc(),
        "price_desc":      Product.price.desc(),
        "name_asc":        Product.name.asc(),
        "created_at_desc": Product.created_at.desc(),
        "created_at_asc":  Product.created_at.asc(),
    }
    query = query.order_by(sort_map.get(sort, Product.created_at.desc()))

    total = query.count()
    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return {
        "items": [product_to_dict(p, db) for p in products],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }


@router.get("/{slug}")
def get_product(slug: str, db: Session = Depends(get_db)):
    p = db.query(Product).options(
        joinedload(Product.images),
        joinedload(Product.category),
    ).filter(Product.slug == slug, Product.is_active == True).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_to_dict(p, db)


@router.post("/")
def create_product(data: ProductCreate, db: Session = Depends(get_db), user=Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product_to_dict(product, db)


@router.put("/{product_id}")
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), user=Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in data.dict(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return product_to_dict(p, db)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    p.is_active = False
    db.commit()
    return {"message": "Product deactivated"}
