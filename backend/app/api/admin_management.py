"""
backend/app/api/admin_management.py  ←  NEW FILE — copy to your app/api/ folder
================================================================================
All routes here require a valid admin JWT (role=admin or superadmin).
Prefix is /api/admin — so full URLs are e.g. /api/admin/products, /api/admin/orders
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import Optional, List
from pydantic import BaseModel
import shutil, os, uuid
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.admin_auth import get_current_admin
from app.models.user import User, Order, OrderItem, Product, Category
import re

router = APIRouter()

# UPLOAD_DIR = "static/images"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# Images are stored per-product: static/images/products/<slug>/<filename>
BASE_STATIC = "static/images/products"
os.makedirs(BASE_STATIC, exist_ok=True)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def safe_val(obj, attr, default=None):
    try:
        v = getattr(obj, attr, default)
        return v.value if hasattr(v, "value") else v
    except Exception:
        return default

def user_dict(u: User):
    return {
        "id": u.id, "name": u.full_name, "email": u.email, "phone": u.phone,
        "is_admin": u.is_admin, "is_active": safe_val(u, "is_active", True),
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }

def product_dict(p: Product):
    imgs = [safe_val(i, "url", "") for i in (p.images or [])] if hasattr(p, "images") else []
    return {
        "id": p.id, "name": p.name, "slug": p.slug,
        "price": p.price, "compare_price": safe_val(p, "compare_price"),
        "stock_qty": safe_val(p, "stock_qty", 0),
        "is_active": safe_val(p, "is_active", True),
        "is_featured": safe_val(p, "is_featured", False),
        "category": safe_val(p.category, "name") if hasattr(p, "category") and p.category else None,
        "category_id": safe_val(p, "category_id"),
        "images": imgs,
        "created_at": p.created_at.isoformat() if hasattr(p, "created_at") and p.created_at else None,
    }

def order_dict(o: Order, db: Session):
    items = []
    for i in (o.items or []):
        items.append({
            "id": i.id, "quantity": i.quantity, "unit_price": i.unit_price, "total": i.total,
            "product_name": safe_val(i.product, "name", "?") if hasattr(i, "product") else "?",
        })
    return {
        "id": o.id, "order_number": o.order_number,
        "status": safe_val(o, "status", "pending"),
        "payment_status": safe_val(o, "payment_status", "pending"),
        "payment_method": safe_val(o, "payment_method", "cod"),
        "subtotal": o.subtotal, "shipping_charge": o.shipping_charge,
        "discount": o.discount, "total": o.total,
        "tracking_number": safe_val(o, "tracking_number"),
        "notes": safe_val(o, "notes"),
        "user_id": o.user_id,
        "user_name": safe_val(o.user, "full_name", "Guest") if hasattr(o, "user") and o.user else "Guest",
        "user_email": safe_val(o.user, "email") if hasattr(o, "user") and o.user else None,
        "ship_name": safe_val(o, "shipping_name"), "ship_phone": safe_val(o, "shipping_phone"),
        "ship_address": safe_val(o, "shipping_line1"), "ship_city": safe_val(o, "shipping_city"),
        "ship_pincode": safe_val(o, "shipping_pincode"), "ship_state": safe_val(o, "shipping_state"),
        "items": items,
        "created_at": o.created_at.isoformat() if o.created_at else None,
    }

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD / ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/dashboard", summary="[Admin] Full dashboard KPIs + charts")
def admin_dashboard(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    total_orders  = db.query(func.count(Order.id)).scalar() or 0
    total_revenue = db.query(func.coalesce(func.sum(Order.total), 0)).scalar() or 0
    total_users   = db.query(func.count(User.id)).filter(User.is_admin == False).scalar() or 0
    total_products= db.query(func.count(Product.id)).scalar() or 0

    # Orders by status
    status_rows = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    by_status = {(s.value if hasattr(s, "value") else s): c for s, c in status_rows}

    # Revenue last 7 days
    seven_days = []
    for i in range(6, -1, -1):
        day = datetime.utcnow().date() - timedelta(days=i)
        rev = db.query(func.coalesce(func.sum(Order.total), 0)).filter(
            func.date(Order.created_at) == day
        ).scalar() or 0
        cnt = db.query(func.count(Order.id)).filter(
            func.date(Order.created_at) == day
        ).scalar() or 0
        seven_days.append({"date": str(day), "revenue": float(rev), "orders": cnt})

    # Top 5 products by revenue
    top_products = db.query(
        Product.name,
        func.coalesce(func.sum(OrderItem.total), 0).label("revenue"),
        func.coalesce(func.sum(OrderItem.quantity), 0).label("units")
    ).join(OrderItem, OrderItem.product_id == Product.id, isouter=True)\
     .group_by(Product.id).order_by(desc("revenue")).limit(5).all()

    # Low stock
    low_stock = db.query(Product).filter(Product.stock_qty <= 10).count() if hasattr(Product, "stock_qty") else 0

    # Pending consultations (if table exists)
    pending_consults = 0
    try:
        from app.models.user import Consultation
        pending_consults = db.query(func.count(Consultation.id)).filter(
            Consultation.status == "pending"
        ).scalar() or 0
    except Exception:
        pass

    # Recent orders
    recent_orders = db.query(Order).options(joinedload(Order.user)).order_by(
        desc(Order.created_at)
    ).limit(5).all()

    return {
        "kpis": {
            "total_orders": total_orders,
            "total_revenue": round(float(total_revenue), 2),
            "total_users": total_users,
            "total_products": total_products,
            "low_stock_products": low_stock,
            "pending_consultations": pending_consults,
            "orders_by_status": by_status,
        },
        "revenue_last_7_days": seven_days,
        "top_products": [{"name": n, "revenue": float(r), "units": int(u)} for n, r, u in top_products],
        "recent_orders": [order_dict(o, db) for o in recent_orders],
    }

@router.get("/analytics/revenue", summary="[Admin] Revenue report (daily/monthly)")
def revenue_report(
    period: str = Query("monthly", enum=["daily", "monthly"]),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    if period == "daily":
        rows = []
        for i in range(29, -1, -1):
            day = datetime.utcnow().date() - timedelta(days=i)
            rev = db.query(func.coalesce(func.sum(Order.total), 0)).filter(
                func.date(Order.created_at) == day
            ).scalar() or 0
            rows.append({"label": str(day), "revenue": float(rev)})
        return rows
    else:
        # Last 12 months
        rows = db.query(
            func.strftime("%Y-%m", Order.created_at).label("month"),
            func.coalesce(func.sum(Order.total), 0).label("revenue"),
            func.count(Order.id).label("orders")
        ).group_by("month").order_by(desc("month")).limit(12).all()
        return [{"label": m, "revenue": float(r), "orders": o} for m, r, o in rows]

# ══════════════════════════════════════════════════════════════════════════════
# USERS
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/users", summary="[Admin] List all consumers")
def list_users(
    search: Optional[str] = None,
    page: int = 1, limit: int = 20,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    q = db.query(User).filter(User.is_admin == False)
    if search:
        q = q.filter(
            User.full_name.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%") |
            User.phone.ilike(f"%{search}%")
        )
    total = q.count()
    users = q.order_by(desc(User.created_at)).offset((page-1)*limit).limit(limit).all()
    return {"total": total, "users": [user_dict(u) for u in users]}

@router.get("/users/{user_id}", summary="[Admin] User detail + order history")
def get_user(user_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    d = user_dict(u)
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).limit(10).all()
    d["recent_orders"] = [{"id": o.id, "order_number": o.order_number,
                            "status": safe_val(o, "status"), "total": o.total,
                            "created_at": o.created_at.isoformat() if o.created_at else None} for o in orders]
    d["total_orders"] = db.query(func.count(Order.id)).filter(Order.user_id == user_id).scalar() or 0
    d["lifetime_value"] = float(db.query(func.coalesce(func.sum(Order.total), 0)).filter(Order.user_id == user_id).scalar() or 0)
    return d

@router.patch("/users/{user_id}/toggle", summary="[Admin] Block/unblock user")
def toggle_user(user_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id, User.is_admin == False).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if hasattr(u, "is_active"):
        u.is_active = not u.is_active
        db.commit()
        return {"message": "User status updated", "is_active": u.is_active}
    return {"message": "is_active field not present on User model — add it first"}

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTS (admin CRUD — supplements existing /api/products public endpoints)
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/products", summary="[Admin] All products incl. inactive")
def admin_list_products(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    low_stock: Optional[bool] = None,
    page: int = 1, limit: int = 20,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    q = db.query(Product).options(joinedload(Product.category)) if hasattr(Product, "category") \
        else db.query(Product)
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%"))
    if category_id:
        q = q.filter(Product.category_id == category_id)
    if low_stock and hasattr(Product, "stock_qty"):
        q = q.filter(Product.stock_qty <= 10)
    total = q.count()
    prods = q.order_by(desc(Product.created_at if hasattr(Product, "created_at") else Product.id))\
             .offset((page-1)*limit).limit(limit).all()
    return {"total": total, "products": [product_dict(p) for p in prods]}

@router.post("/products", summary="[Admin] Create new product")
def admin_create_product(
    data: dict,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Create a new product.
    Required: name, price, category_id, slug
    Optional: sku, description, story, healing_props, chakra, zodiac, origin, 
              weight_grams, dimensions, compare_price, stock_qty, is_active, is_featured,
              is_bestseller, is_new_arrival, meta_title, meta_desc
    """
    # Validate required fields
    if not data.get("name"):
        raise HTTPException(status_code=400, detail="Product name is required")
    if data.get("price") is None:
        raise HTTPException(status_code=400, detail="Price is required")
    if not data.get("category_id"):
        raise HTTPException(status_code=400, detail="Category is required")
    if not data.get("slug"):
        raise HTTPException(status_code=400, detail="Slug is required")
    
    # Check if slug is unique
    existing = db.query(Product).filter(Product.slug == data["slug"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    
    # Check if category exists
    category = db.query(Category).filter(Category.id == data["category_id"]).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if SKU is unique (if provided)
    if data.get("sku"):
        existing_sku = db.query(Product).filter(Product.sku == data["sku"]).first()
        if existing_sku:
            raise HTTPException(status_code=400, detail="SKU already exists")
    
    # Create product
    allowed_fields = {
        "name", "slug", "sku", "category_id", "description", "story", "healing_props",
        "chakra", "zodiac", "origin", "weight_grams", "dimensions", "price", "compare_price",
        "stock_qty", "is_active", "is_featured", "is_bestseller", "is_new_arrival",
        "meta_title", "meta_desc"
    }
    
    product_data = {k: v for k, v in data.items() if k in allowed_fields and v is not None}
    p = Product(**product_data)
    
    db.add(p)
    db.commit()
    db.refresh(p)
    
    return {"message": "Product created", "product_id": p.id, "product": product_dict(p)}

@router.patch("/products/{product_id}", summary="[Admin] Update product fields")
def admin_update_product(
    product_id: int,
    data: dict,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    # allowed = {"name", "price", "compare_price", "stock_qty", "is_active", "is_featured",
    #            "description", "category_id", "slug"}
    allowed = {"name", "price", "compare_price", "stock_qty", "is_active", "is_featured",
               "description", "category_id", "slug", "sku", "story", "healing_props",
               "chakra", "zodiac", "origin", "weight_grams", "dimensions",
               "is_bestseller", "is_new_arrival", "meta_title", "meta_desc"}
    
    # Check slug uniqueness if being updated
    if "slug" in data and data["slug"] != p.slug:
        existing = db.query(Product).filter(Product.slug == data["slug"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists")
    
    # Check SKU uniqueness if being updated
    if "sku" in data and data["sku"] != p.sku:
        existing_sku = db.query(Product).filter(Product.sku == data["sku"]).first()
        if existing_sku:
            raise HTTPException(status_code=400, detail="SKU already exists")
        
    for k, v in data.items():
        if k in allowed and hasattr(p, k):
            setattr(p, k, v)
    db.commit()
    return {"message": "Product updated"}

@router.post("/products/{product_id}/image", summary="[Admin] Upload product image")
async def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Upload an image for a product.
    - Saves to  static/images/products/<product-slug>/<unique-filename>
    - Records the URL in product_images table (is_primary=True if first image)
    - Returns the image URL and new image record id
    """

    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # ext = os.path.splitext(file.filename)[1] or ".jpg"
    # filename = f"product_{product_id}_{uuid.uuid4().hex[:8]}{ext}"
    # filepath = os.path.join(UPLOAD_DIR, filename)
    # with open(filepath, "wb") as f:
    #     shutil.copyfileobj(file.file, f)
    # image_url = f"/static/images/{filename}"
    # # If your Product model has an images relationship, add the image there
    # # Otherwise just return the URL for manual update
    # try:
    #     from app.models.user import ProductImage
    #     img = ProductImage(product_id=product_id, url=image_url)
    #     db.add(img)
    #     db.commit()
    # except Exception:
    #     pass
    # return {"message": "Image uploaded", "url": image_url}
    # Create product-specific folder: static/images/products/<slug>/
    safe_slug = re.sub(r"[^a-z0-9_-]", "_", (p.slug or f"product_{product_id}").lower())
    product_folder = os.path.join(BASE_STATIC, safe_slug)
    os.makedirs(product_folder, exist_ok=True)

    # Unique filename
    ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
    filename = f"{uuid.uuid4().hex[:10]}{ext}"
    filepath = os.path.join(product_folder, filename)

    # Save file to disk
    with open(filepath, "wb") as out:
        shutil.copyfileobj(file.file, out)

    # URL that the frontend/static server will serve
    image_url = f"/static/images/products/{safe_slug}/{filename}"

    # Determine sort_order and whether this is the first (primary) image
    from app.models.user import ProductImage
    existing_count = db.query(ProductImage).filter(
        ProductImage.product_id == product_id
    ).count()
    is_primary = existing_count == 0   # first upload becomes primary

    img = ProductImage(
        product_id=product_id,
        url=image_url,
        is_primary=is_primary,
        sort_order=existing_count,
        alt_text=p.name
    )
    db.add(img)
    db.commit()
    db.refresh(img)

    return {
        "message": "Image uploaded successfully",
        "id": img.id,
        "url": image_url,
        "is_primary": is_primary,
        "sort_order": img.sort_order
    }

@router.delete("/products/{product_id}/images/{image_id}", summary="[Admin] Delete a product image")
def delete_product_image(
    product_id: int,
    image_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Delete an image record AND its file from disk.
    If the deleted image was primary, promotes the next image to primary.
    """
    from app.models.user import ProductImage
    img = db.query(ProductImage).filter(
        ProductImage.id == image_id,
        ProductImage.product_id == product_id
    ).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")

    was_primary = img.is_primary

    # Delete file from disk if it's a local static file
    if img.url and img.url.startswith("/static/"):
        disk_path = img.url.lstrip("/")   # "static/images/products/..."
        if os.path.isfile(disk_path):
            os.remove(disk_path)

    db.delete(img)
    db.flush()

    # If we deleted the primary, promote the next image
    if was_primary:
        next_img = db.query(ProductImage).filter(
            ProductImage.product_id == product_id
        ).order_by(ProductImage.sort_order).first()
        if next_img:
            next_img.is_primary = True

    db.commit()
    return {"message": "Image deleted", "image_id": image_id}


@router.patch("/products/{product_id}/images/{image_id}/set-primary", summary="[Admin] Set image as primary")
def set_primary_image(
    product_id: int,
    image_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Mark one image as primary (card listing image).
    Clears is_primary on all other images for this product.
    """
    from app.models.user import ProductImage
    # Clear all primary flags for this product
    db.query(ProductImage).filter(
        ProductImage.product_id == product_id
    ).update({"is_primary": False})

    # Set the chosen one as primary
    img = db.query(ProductImage).filter(
        ProductImage.id == image_id,
        ProductImage.product_id == product_id
    ).first()
    if not img:
        db.rollback()
        raise HTTPException(status_code=404, detail="Image not found")
    img.is_primary = True
    db.commit()
    return {"message": "Primary image updated", "image_id": image_id}


@router.get("/products/{product_id}/images", summary="[Admin] List all images for a product")
def list_product_images(
    product_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Return all images for a product sorted by sort_order."""
    from app.models.user import ProductImage
    imgs = db.query(ProductImage).filter(
        ProductImage.product_id == product_id
    ).order_by(ProductImage.sort_order).all()
    return [
        {
            "id": i.id,
            "url": i.url,
            "is_primary": i.is_primary,
            "sort_order": i.sort_order,
            "alt_text": i.alt_text
        }
        for i in imgs
    ]

@router.delete("/products/{product_id}", summary="[Admin] Soft-delete product (set inactive)")
def admin_delete_product(product_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    if hasattr(p, "is_active"):
        p.is_active = False
        db.commit()
        return {"message": "Product deactivated"}
    raise HTTPException(status_code=400, detail="Product model has no is_active field")

# ══════════════════════════════════════════════════════════════════════════════
# ORDERS (admin view — full control)
# ══════════════════════════════════════════════════════════════════════════════

VALID_STATUSES = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled", "refunded"]

@router.get("/orders", summary="[Admin] All orders with filters")
def admin_list_orders(
    status: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 1, limit: int = 20,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    q = db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.items).joinedload(OrderItem.product)
    )
    if status:
        q = q.filter(Order.status == status)
    if search:
        q = q.filter(Order.order_number.ilike(f"%{search}%"))
    if date_from:
        q = q.filter(func.date(Order.created_at) >= date_from)
    if date_to:
        q = q.filter(func.date(Order.created_at) <= date_to)
    total = q.count()
    orders_list = q.order_by(desc(Order.created_at)).offset((page-1)*limit).limit(limit).all()
    return {"total": total, "orders": [order_dict(o, db) for o in orders_list]}

@router.get("/orders/{order_id}", summary="[Admin] Single order detail")
def admin_get_order(order_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    o = db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_dict(o, db)

@router.patch("/orders/{order_id}/status", summary="[Admin] Update order status")
def admin_update_order_status(
    order_id: int,
    data: dict,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    new_status = data.get("status")
    if new_status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Status must be one of {VALID_STATUSES}")
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    o.status = new_status
    if tracking := data.get("tracking_number"):
        if hasattr(o, "tracking_number"):
            o.tracking_number = tracking
    db.commit()
    return {"message": f"Order status updated to {new_status}"}

@router.patch("/orders/{order_id}/payment", summary="[Admin] Update payment status")
def admin_update_payment(
    order_id: int, data: dict,
    admin=Depends(get_current_admin), db: Session = Depends(get_db)
):
    o = db.query(Order).filter(Order.id == order_id).first()
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    if hasattr(o, "payment_status"):
        o.payment_status = data.get("payment_status", o.payment_status)
    db.commit()
    return {"message": "Payment status updated"}

# ══════════════════════════════════════════════════════════════════════════════
# CONSULTATIONS
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/consultations", summary="[Admin] All consultation bookings")
def admin_list_consultations(
    status: Optional[str] = None,
    page: int = 1, limit: int = 20,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        from app.models.user import Consultation
        q = db.query(Consultation)
        if status:
            q = q.filter(Consultation.status == status)
        total = q.count()
        rows = q.order_by(desc(Consultation.created_at)).offset((page-1)*limit).limit(limit).all()
        return {"total": total, "consultations": [
            {"id": c.id, "name": c.name, "email": c.email, "phone": c.phone,
             "subject": safe_val(c, "subject", ""), "message": safe_val(c, "message"),
             "preferred_date": safe_val(c, "preferred_date"), "preferred_time": safe_val(c, "preferred_time"),
             "status": safe_val(c, "status", "pending"), "admin_notes": safe_val(c, "admin_notes"),
             "created_at": c.created_at.isoformat() if c.created_at else None}
            for c in rows
        ]}
    except ImportError:
        return {"total": 0, "consultations": [],
                "note": "Consultation model not found — add it to app/models/user.py"}

@router.patch("/consultations/{consult_id}", summary="[Admin] Update consultation")
def admin_update_consultation(
    consult_id: int, data: dict,
    admin=Depends(get_current_admin), db: Session = Depends(get_db)
):
    try:
        from app.models.user import Consultation
        c = db.query(Consultation).filter(Consultation.id == consult_id).first()
        if not c:
            raise HTTPException(status_code=404, detail="Consultation not found")
        for k in ("status", "admin_notes", "preferred_date", "preferred_time"):
            if k in data and hasattr(c, k):
                setattr(c, k, data[k])
        db.commit()
        return {"message": "Consultation updated"}
    except ImportError:
        raise HTTPException(status_code=404, detail="Consultation model not found")

# ══════════════════════════════════════════════════════════════════════════════
# INVENTORY REPORT
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/inventory", summary="[Admin] Inventory + low-stock report")
def inventory_report(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    prods = db.query(Product).options(
        joinedload(Product.category) if hasattr(Product, "category") else None
    ).all()
    all_p = [product_dict(p) for p in prods]
    low = [p for p in all_p if (p.get("stock_qty") or 0) <= 10]
    out = [p for p in all_p if (p.get("stock_qty") or 0) == 0]
    return {
        "total_products": len(all_p),
        "low_stock": low,
        "out_of_stock": out,
        "all_products": all_p,
    }

# ══════════════════════════════════════════════════════════════════════════════
# REVIEWS MODERATION
# ══════════════════════════════════════════════════════════════════════════════

@router.get("/reviews", summary="[Admin] All reviews")
def admin_list_reviews(
    approved: Optional[int] = None,
    page: int = 1, limit: int = 30,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        from app.models.user import Review
        q = db.query(Review)
        if approved is not None:
            q = q.filter(Review.is_approved == bool(approved))
        total = q.count()
        rows = q.order_by(desc(Review.created_at if hasattr(Review, "created_at") else Review.id))\
                .offset((page-1)*limit).limit(limit).all()
        return {"total": total, "reviews": [
            {"id": r.id, "rating": r.rating, "title": safe_val(r, "title"),
             "body": safe_val(r, "body"), "is_approved": safe_val(r, "is_approved", False),
             "product_id": safe_val(r, "product_id"), "user_id": safe_val(r, "user_id")}
            for r in rows
        ]}
    except ImportError:
        return {"total": 0, "reviews": [], "note": "Review model not found"}

@router.patch("/reviews/{review_id}/approve", summary="[Admin] Approve a review")
def approve_review(review_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        from app.models.user import Review
        r = db.query(Review).filter(Review.id == review_id).first()
        if not r:
            raise HTTPException(status_code=404, detail="Review not found")
        r.is_approved = True
        db.commit()
        return {"message": "Review approved"}
    except ImportError:
        raise HTTPException(status_code=404, detail="Review model not found")
