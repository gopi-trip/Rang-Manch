from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, func
from model import (ReviewCreate, ReviewRead, ReviewUpate, Review)
from database import get_session

router = APIRouter(prefix="/review",tags=["reviews"])

@router.post("/",response_model=ReviewRead)
def create_review(review:ReviewCreate,session:Session = Depends(get_session)):
    db_review = Review(**review.model_dump()) 
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review

@router.get("/",response_model=list[ReviewRead])
def get_reviews(
    play_name: str | None = Query(default=None, description="Filter by the play name"),
    skip: int = Query(default=0,ge=0,description="No. of reviews to skip/offset"),
    limit: int = Query(default=10,ge=1,le=50,description="Max. no. of reviews to return"),
    session: Session = Depends(get_session)
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query = query.offset(skip).limit(limit)

    reviews = session.exec(query).all()

    return reviews