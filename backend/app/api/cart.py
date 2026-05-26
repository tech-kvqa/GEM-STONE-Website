from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.core.security import require_user
from app.models.user import CartItem, Product
from app.api.products import product_to_dict

router = APIRouter()

def cart_item_to_dict(item: CartItem, db: Session) -> dict:
    return {
        "id": item.id,
        "quantity": item.quantity,
        "product": product_to_dict(item.product, db),
    }

def load_cart(user_id: int, db: Session):
    return db.query(CartItem).options(
        joinedload(CartItem.product).joinedload(Product.images),
        joinedload(CartItem.product).joinedload(Product.category),
    ).filter(CartItem.user_id == user_id).all()


@router.get("/")
def get_cart(db: Session = Depends(get_db), user=Depends(require_user)):
    items = load_cart(user.id, db)
    return [cart_item_to_dict(i, db) for i in items]


@router.post("/")
def add_to_cart(data: dict, db: Session = Depends(get_db), user=Depends(require_user)):
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_qty < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    existing = db.query(CartItem).filter(
        CartItem.user_id == user.id, CartItem.product_id == product_id
    ).first()

    if existing:
        existing.quantity = min(existing.quantity + quantity, product.stock_qty)
        db.commit()
        db.refresh(existing)
        item = db.query(CartItem).options(
            joinedload(CartItem.product).joinedload(Product.images),
            joinedload(CartItem.product).joinedload(Product.category),
        ).filter(CartItem.id == existing.id).first()
        return cart_item_to_dict(item, db)
    else:
        new_item = CartItem(user_id=user.id, product_id=product_id, quantity=quantity)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        item = db.query(CartItem).options(
            joinedload(CartItem.product).joinedload(Product.images),
            joinedload(CartItem.product).joinedload(Product.category),
        ).filter(CartItem.id == new_item.id).first()
        return cart_item_to_dict(item, db)


@router.put("/{item_id}")
def update_cart_item(item_id: int, data: dict, db: Session = Depends(get_db), user=Depends(require_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    quantity = data.get("quantity", 1)
    if quantity <= 0:
        db.delete(item)
        db.commit()
        return {"message": "Item removed"}
    item.quantity = quantity
    db.commit()
    loaded = db.query(CartItem).options(
        joinedload(CartItem.product).joinedload(Product.images),
        joinedload(CartItem.product).joinedload(Product.category),
    ).filter(CartItem.id == item_id).first()
    return cart_item_to_dict(loaded, db)


@router.delete("/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    return {"message": "Removed from cart"}


@router.delete("/")
def clear_cart(db: Session = Depends(get_db), user=Depends(require_user)):
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
