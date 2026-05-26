"""
backend/app/api/admin_auth.py  ←  NEW FILE — copy to your app/api/ folder
=========================================================================
Admin login is a SEPARATE endpoint from consumer login.
It checks the same User table but requires is_admin=True.
JWT tokens carry  "role": "admin"  so consumer tokens cannot access admin APIs.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.models.user import User

router = APIRouter()
bearer = HTTPBearer(auto_error=False)

# ─── Schemas ──────────────────────────────────────────────────────────────────
class AdminLoginIn(BaseModel):
    email: EmailStr
    password: str

class AdminCreateIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "admin"           # "admin" | "superadmin"

# ─── Admin JWT guard (used by admin_management.py too) ───────────────────────
def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Admin token required")
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("role") not in ("admin", "superadmin"):
            raise HTTPException(status_code=403, detail="Admin access required")
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")

    user = db.query(User).filter(User.email == email, User.is_admin == True).first()
    if not user:
        raise HTTPException(status_code=401, detail="Admin account not found or deactivated")
    return user

def require_superadmin(admin: User = Depends(get_current_admin)):
    if getattr(admin, "admin_role", "admin") != "superadmin":
        raise HTTPException(status_code=403, detail="Superadmin access required")
    return admin

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.post("/login", summary="Admin login — separate from consumer login")
def admin_login(data: AdminLoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.is_admin == True).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    # Embed role=admin into JWT so it's distinguishable from consumer tokens
    token = create_access_token({
        "sub": user.email,
        "role": getattr(user, "admin_role", "admin"),
        "type": "admin"
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "admin": {
            "id":       user.id,
            "name":     user.full_name,
            "email":    user.email,
            "role":     getattr(user, "admin_role", "admin"),
            "is_admin": True,
        }
    }

@router.get("/me", summary="Get logged-in admin profile")
def admin_me(admin: User = Depends(get_current_admin)):
    return {
        "id":       admin.id,
        "name":     admin.full_name,
        "email":    admin.email,
        "phone":    admin.phone,
        "role":     getattr(admin, "admin_role", "admin"),
        "is_admin": True,
        "created_at": admin.created_at.isoformat() if admin.created_at else None,
    }

@router.get("/list", summary="List all admin accounts [superadmin only]")
def list_admins(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    admins = db.query(User).filter(User.is_admin == True).all()
    return [{"id": a.id, "name": a.full_name, "email": a.email,
             "role": getattr(a, "admin_role", "admin"),
             "is_active": a.is_active if hasattr(a, "is_active") else True} for a in admins]

@router.post("/create", summary="Create a new admin account [superadmin only]")
def create_admin(data: AdminCreateIn, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_admin = User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=get_password_hash(data.password),
        is_admin=True,
    )
    if hasattr(User, "admin_role"):
        new_admin.admin_role = data.role
    db.add(new_admin)
    db.commit()
    return {"message": f"Admin '{data.full_name}' created successfully"}
