# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# import os

# from app.api import products, categories, cart, orders, auth, wishlist, reviews
# from app.core.database import engine, Base

# Base.metadata.create_all(bind=engine)

# app = FastAPI(
#     title="Crystal Luxe API",
#     description="Premium Crystal & Gemstone E-Commerce Platform",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount static files for product images
# os.makedirs("static/images", exist_ok=True)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Register routers
# app.include_router(auth.router,       prefix="/api/auth",       tags=["Authentication"])
# app.include_router(products.router,   prefix="/api/products",   tags=["Products"])
# app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
# app.include_router(cart.router,       prefix="/api/cart",       tags=["Cart"])
# app.include_router(orders.router,     prefix="/api/orders",     tags=["Orders"])
# app.include_router(wishlist.router,   prefix="/api/wishlist",   tags=["Wishlist"])
# app.include_router(reviews.router,    prefix="/api/reviews",    tags=["Reviews"])

# @app.get("/")
# def root():
#     return {"message": "Welcome to Crystal Luxe API", "status": "running"}

# @app.get("/health")
# def health_check():
#     return {"status": "healthy"}


"""
backend/app/main.py  ←  REPLACE YOUR EXISTING main.py WITH THIS
=================================================================
Changes vs original:
  • Added admin auth router  (/api/admin/auth)
  • Added admin management router  (/api/admin/*)
  • Everything else unchanged — all original routes still work
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import subprocess
import sys

# ── Original routers (unchanged) ──────────────────────────────────────────────
from app.api import products, categories, cart, orders, auth, wishlist, reviews
from app.core.database import engine, Base

# ── New admin routers ──────────────────────────────────────────────────────────
from app.api import admin_auth, admin_management

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crystal Luxe API",
    description="Premium Crystal & Gemstone E-Commerce Platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/images", exist_ok=True)
os.makedirs("static/images/categories", exist_ok=True)
os.makedirs("static/images/products", exist_ok=True)
os.makedirs("static/images/banners", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── AUTO SEED ON STARTUP ─────────────────────────────────────────────────────

@app.on_event("startup")
def startup_seed():
    """
    Automatically runs seed.py on backend startup.
    Correctly resolves path from app/main.py → backend/seed.py
    """
    try:
        # Move one folder up from /app/main.py → /backend/
        backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        seed_file = os.path.join(backend_root, "seed.py")

        if os.path.exists(seed_file):
            print(f"🌱 Running automatic database seed from: {seed_file}")

            subprocess.run(
                [sys.executable, seed_file],
                cwd=backend_root,   # ensures relative paths work
                check=True
            )

            print("✅ Database seeded successfully.")
        else:
            print(f"⚠ seed.py not found at: {seed_file}")

    except Exception as e:
        print(f"❌ Seed failed: {e}")

# ── Original routes (unchanged) ───────────────────────────────────────────────
app.include_router(auth.router,             prefix="/api/auth",             tags=["Consumer Auth"])
app.include_router(products.router,         prefix="/api/products",         tags=["Products"])
app.include_router(categories.router,       prefix="/api/categories",       tags=["Categories"])
app.include_router(cart.router,             prefix="/api/cart",             tags=["Cart"])
app.include_router(orders.router,           prefix="/api/orders",           tags=["Orders"])
app.include_router(wishlist.router,         prefix="/api/wishlist",         tags=["Wishlist"])
app.include_router(reviews.router,          prefix="/api/reviews",          tags=["Reviews"])

# ── NEW: Admin routes ─────────────────────────────────────────────────────────
app.include_router(admin_auth.router,       prefix="/api/admin/auth",       tags=["Admin Auth"])
app.include_router(admin_management.router, prefix="/api/admin",            tags=["Admin Management"])

@app.get("/")
def root():
    return {"message": "Crystal Luxe API v2 — Admin + Consumer", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
