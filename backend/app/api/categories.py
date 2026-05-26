from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import require_user
from app.models.user import Category
from app.schemas.schemas import CategoryOut, CategoryCreate

router = APIRouter()

@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.is_active == True).order_by(Category.sort_order).all()

@router.get("/{slug}", response_model=CategoryOut)
def get_category(slug: str, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.slug == slug, Category.is_active == True).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), user=Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    cat = Category(**data.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.put("/{cat_id}", response_model=CategoryOut)
def update_category(cat_id: int, data: dict, db: Session = Depends(get_db), user=Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403)
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404)
    for k, v in data.items():
        setattr(cat, k, v)
    db.commit()
    db.refresh(cat)
    return cat
