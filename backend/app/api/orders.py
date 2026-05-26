from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid
from app.core.database import get_db
from app.core.security import require_user
from app.models.user import Order, OrderItem, CartItem, Product, Address
from app.api.products import product_to_dict

router = APIRouter()

def generate_order_number():
    return f"CL-{uuid.uuid4().hex[:8].upper()}"

def order_item_to_dict(item: OrderItem, db: Session) -> dict:
    return {
        "id": item.id,
        "quantity": item.quantity,
        "unit_price": item.unit_price,
        "total": item.total,
        "product": product_to_dict(item.product, db),
    }

def order_to_dict(order: Order, db: Session) -> dict:
    return {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status.value if hasattr(order.status, 'value') else order.status,
        "subtotal": order.subtotal,
        "shipping_charge": order.shipping_charge,
        "discount": order.discount,
        "total": order.total,
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "tracking_number": order.tracking_number,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "items": [order_item_to_dict(i, db) for i in order.items],
    }

def load_order(order_id: int, db: Session) -> Order:
    return db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.images),
        joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.category),
    ).filter(Order.id == order_id).first()


@router.get("/")
def list_orders(db: Session = Depends(get_db), user=Depends(require_user)):
    orders = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.images),
        joinedload(Order.items).joinedload(OrderItem.product).joinedload(Product.category),
    ).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()
    return [order_to_dict(o, db) for o in orders]


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    order = load_order(order_id, db)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_to_dict(order, db)


@router.post("/")
def place_order(data: dict, db: Session = Depends(get_db), user=Depends(require_user)):
    cart_items = db.query(CartItem).options(joinedload(CartItem.product)).filter(
        CartItem.user_id == user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart_items:
        if item.product.stock_qty < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {item.product.name}")

    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 0 if subtotal >= 999 else 99
    total = subtotal + shipping

    order = Order(
        order_number=generate_order_number(),
        user_id=user.id,
        subtotal=subtotal,
        shipping_charge=shipping,
        discount=0,
        total=total,
        payment_method=data.get("payment_method", "cod"),
        notes=data.get("notes"),
        shipping_name=data.get("shipping_name"),
        shipping_phone=data.get("shipping_phone"),
        shipping_line1=data.get("shipping_line1"),
        shipping_line2=data.get("shipping_line2"),
        shipping_city=data.get("shipping_city"),
        shipping_state=data.get("shipping_state"),
        shipping_pincode=data.get("shipping_pincode"),
        shipping_country=data.get("shipping_country", "India"),
    )
    db.add(order)
    db.flush()

    for item in cart_items:
        oi = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
            total=item.product.price * item.quantity
        )
        db.add(oi)
        item.product.stock_qty -= item.quantity

    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()

    loaded = load_order(order.id, db)
    return order_to_dict(loaded, db)


@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    order = load_order(order_id, db)
    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")
    status_val = order.status.value if hasattr(order.status, 'value') else order.status
    if status_val not in ("pending", "confirmed"):
        raise HTTPException(status_code=400, detail="Order cannot be cancelled at this stage")
    order.status = "cancelled"
    for item in order.items:
        item.product.stock_qty += item.quantity
    db.commit()
    return {"message": "Order cancelled"}
