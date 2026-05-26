from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    full_name     = Column(String(100), nullable=False)
    email         = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone         = Column(String(20))
    is_active     = Column(Boolean, default=True)
    is_admin      = Column(Boolean, default=False)
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, onupdate=func.now())

    addresses  = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders     = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")
    wishlist   = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")
    reviews    = relationship("Review", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    label      = Column(String(50), default="Home")
    full_name  = Column(String(100), nullable=False)
    phone      = Column(String(20), nullable=False)
    line1      = Column(String(255), nullable=False)
    line2      = Column(String(255))
    city       = Column(String(100), nullable=False)
    state      = Column(String(100), nullable=False)
    pincode    = Column(String(10), nullable=False)
    country    = Column(String(100), default="India")
    is_default = Column(Boolean, default=False)

    user = relationship("User", back_populates="addresses")

class Category(Base):
    __tablename__ = "categories"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), unique=True, nullable=False)
    slug        = Column(String(120), unique=True, nullable=False)
    description = Column(Text)
    story       = Column(Text)      # Brand story for each category
    image_url   = Column(String(500))
    banner_url  = Column(String(500))
    sort_order  = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(255), nullable=False)
    slug           = Column(String(280), unique=True, nullable=False)
    sku            = Column(String(100), unique=True)
    category_id    = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description    = Column(Text)
    story          = Column(Text)         # Crystal story / metaphysical properties
    healing_props  = Column(Text)         # Healing properties
    chakra         = Column(String(100))  # Associated chakra
    zodiac         = Column(String(100))  # Associated zodiac signs
    origin         = Column(String(100))  # Country/region of origin
    weight_grams   = Column(Float)
    dimensions     = Column(String(100))
    price          = Column(Float, nullable=False)
    compare_price  = Column(Float)        # Original/MRP price
    stock_qty      = Column(Integer, default=0)
    is_active      = Column(Boolean, default=True)
    is_featured    = Column(Boolean, default=False)
    is_bestseller  = Column(Boolean, default=False)
    is_new_arrival = Column(Boolean, default=False)
    meta_title     = Column(String(255))
    meta_desc      = Column(Text)
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, onupdate=func.now())

    category   = relationship("Category", back_populates="products")
    images     = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    wishlist   = relationship("WishlistItem", back_populates="product")
    reviews    = relationship("Review", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"

    id         = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url        = Column(String(500), nullable=False)
    alt_text   = Column(String(255))
    sort_order = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)

    product = relationship("Product", back_populates="images")

class CartItem(Base):
    __tablename__ = "cart_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())

    user    = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

class WishlistItem(Base):
    __tablename__ = "wishlist_items"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user    = relationship("User", back_populates="wishlist")
    product = relationship("Product", back_populates="wishlist")

class OrderStatus(str, enum.Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    PACKED    = "packed"
    SHIPPED   = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED  = "refunded"

class Order(Base):
    __tablename__ = "orders"

    id               = Column(Integer, primary_key=True, index=True)
    order_number     = Column(String(50), unique=True, nullable=False)
    user_id          = Column(Integer, ForeignKey("users.id"), nullable=False)
    status           = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    subtotal         = Column(Float, nullable=False)
    shipping_charge  = Column(Float, default=0)
    discount         = Column(Float, default=0)
    total            = Column(Float, nullable=False)
    coupon_code      = Column(String(50))
    shipping_name    = Column(String(100))
    shipping_phone   = Column(String(20))
    shipping_line1   = Column(String(255))
    shipping_line2   = Column(String(255))
    shipping_city    = Column(String(100))
    shipping_state   = Column(String(100))
    shipping_pincode = Column(String(10))
    shipping_country = Column(String(100), default="India")
    payment_method   = Column(String(50))
    payment_id       = Column(String(100))
    payment_status   = Column(String(50), default="pending")
    tracking_number  = Column(String(100))
    notes            = Column(Text)
    created_at       = Column(DateTime, server_default=func.now())
    updated_at       = Column(DateTime, onupdate=func.now())

    user   = relationship("User", back_populates="orders")
    items  = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total      = Column(Float, nullable=False)

    order   = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"

    id         = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating     = Column(Integer, nullable=False)  # 1-5
    title      = Column(String(200))
    body       = Column(Text)
    is_verified = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    created_at  = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="reviews")
    user    = relationship("User", back_populates="reviews")
