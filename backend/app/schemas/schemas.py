from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ── Auth ──────────────────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    is_admin: bool
    created_at: datetime
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# ── Category ──────────────────────────────────────────────────────────────────
class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    story: Optional[str]
    image_url: Optional[str]
    banner_url: Optional[str]
    sort_order: int
    class Config: from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    story: Optional[str] = None
    image_url: Optional[str] = None
    banner_url: Optional[str] = None
    sort_order: int = 0

# ── Product ───────────────────────────────────────────────────────────────────
class ProductImageOut(BaseModel):
    id: int
    url: str
    alt_text: Optional[str]
    is_primary: bool
    sort_order: int
    class Config: from_attributes = True

class ProductSummary(BaseModel):
    id: int
    name: str
    slug: str
    price: float
    compare_price: Optional[float]
    is_featured: bool
    is_bestseller: bool
    is_new_arrival: bool
    stock_qty: int
    category: CategoryOut
    images: List[ProductImageOut] = []
    avg_rating: Optional[float] = None
    review_count: int = 0
    class Config: from_attributes = True

class ProductDetail(ProductSummary):
    description: Optional[str]
    story: Optional[str]
    healing_props: Optional[str]
    chakra: Optional[str]
    zodiac: Optional[str]
    origin: Optional[str]
    weight_grams: Optional[float]
    dimensions: Optional[str]
    sku: Optional[str]
    class Config: from_attributes = True

class ProductCreate(BaseModel):
    name: str
    slug: str
    sku: Optional[str] = None
    category_id: int
    description: Optional[str] = None
    story: Optional[str] = None
    healing_props: Optional[str] = None
    chakra: Optional[str] = None
    zodiac: Optional[str] = None
    origin: Optional[str] = None
    weight_grams: Optional[float] = None
    dimensions: Optional[str] = None
    price: float
    compare_price: Optional[float] = None
    stock_qty: int = 0
    is_featured: bool = False
    is_bestseller: bool = False
    is_new_arrival: bool = False

class ProductUpdate(ProductCreate):
    name: Optional[str] = None
    slug: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None

# ── Cart ──────────────────────────────────────────────────────────────────────
class CartItemOut(BaseModel):
    id: int
    product: ProductSummary
    quantity: int
    class Config: from_attributes = True

class CartAddItem(BaseModel):
    product_id: int
    quantity: int = 1

class CartUpdate(BaseModel):
    quantity: int

# ── Wishlist ──────────────────────────────────────────────────────────────────
class WishlistItemOut(BaseModel):
    id: int
    product: ProductSummary
    class Config: from_attributes = True

# ── Address ───────────────────────────────────────────────────────────────────
class AddressCreate(BaseModel):
    label: str = "Home"
    full_name: str
    phone: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    pincode: str
    country: str = "India"
    is_default: bool = False

class AddressOut(AddressCreate):
    id: int
    class Config: from_attributes = True

# ── Order ─────────────────────────────────────────────────────────────────────
class OrderItemOut(BaseModel):
    id: int
    product: ProductSummary
    quantity: int
    unit_price: float
    total: float
    class Config: from_attributes = True

class OrderOut(BaseModel):
    id: int
    order_number: str
    status: str
    subtotal: float
    shipping_charge: float
    discount: float
    total: float
    payment_method: Optional[str]
    payment_status: str
    tracking_number: Optional[str]
    items: List[OrderItemOut] = []
    created_at: datetime
    class Config: from_attributes = True

class OrderCreate(BaseModel):
    address_id: Optional[int] = None
    shipping_name: Optional[str] = None
    shipping_phone: Optional[str] = None
    shipping_line1: Optional[str] = None
    shipping_city: Optional[str] = None
    shipping_state: Optional[str] = None
    shipping_pincode: Optional[str] = None
    payment_method: str = "cod"
    notes: Optional[str] = None
    coupon_code: Optional[str] = None

# ── Review ────────────────────────────────────────────────────────────────────
class ReviewCreate(BaseModel):
    rating: int
    title: Optional[str] = None
    body: Optional[str] = None

    @validator("rating")
    def rating_range(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

class ReviewOut(BaseModel):
    id: int
    rating: int
    title: Optional[str]
    body: Optional[str]
    is_verified: bool
    created_at: datetime
    user: UserOut
    class Config: from_attributes = True
