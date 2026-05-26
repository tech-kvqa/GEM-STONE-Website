from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.security import require_user
from app.models.user import WishlistItem, Product
from app.api.products import product_to_dict

router = APIRouter()

@router.get("/")
def get_wishlist(db: Session = Depends(get_db), user=Depends(require_user)):
    items = db.query(WishlistItem).options(
        joinedload(WishlistItem.product).joinedload(Product.images),
        joinedload(WishlistItem.product).joinedload(Product.category),
    ).filter(WishlistItem.user_id == user.id).all()
    return [{"id": i.id, "product": product_to_dict(i.product, db)} for i in items]

@router.post("/{product_id}")
def add_to_wishlist(product_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == user.id, WishlistItem.product_id == product_id
    ).first()
    if existing:
        return {"message": "Already in wishlist"}
    item = WishlistItem(user_id=user.id, product_id=product_id)
    db.add(item)
    db.commit()
    return {"message": "Added to wishlist"}

@router.delete("/{product_id}")
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == user.id, WishlistItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not in wishlist")
    db.delete(item)
    db.commit()
    return {"message": "Removed from wishlist"}
