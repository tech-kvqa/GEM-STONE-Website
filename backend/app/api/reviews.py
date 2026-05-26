from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.security import require_user
from app.models.user import Review, Product

router = APIRouter()

def review_to_dict(r: Review) -> dict:
    return {
        "id": r.id,
        "rating": r.rating,
        "title": r.title,
        "body": r.body,
        "is_verified": r.is_verified,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "user": {
            "id": r.user.id,
            "full_name": r.user.full_name,
            "email": r.user.email,
        } if r.user else None,
    }

@router.get("/product/{product_id}")
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).options(joinedload(Review.user)).filter(
        Review.product_id == product_id
    ).order_by(Review.created_at.desc()).all()
    return [review_to_dict(r) for r in reviews]

@router.post("/product/{product_id}")
def add_review(product_id: int, data: dict, db: Session = Depends(get_db), user=Depends(require_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing = db.query(Review).filter(
        Review.product_id == product_id, Review.user_id == user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already reviewed this product")
    rating = data.get("rating")
    if not rating or not (1 <= int(rating) <= 5):
        raise HTTPException(status_code=422, detail="Rating must be between 1 and 5")
    review = Review(
        product_id=product_id,
        user_id=user.id,
        rating=int(rating),
        title=data.get("title"),
        body=data.get("body"),
    )
    db.add(review)
    db.commit()
    r = db.query(Review).options(joinedload(Review.user)).filter(Review.id == review.id).first()
    return review_to_dict(r)

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}
