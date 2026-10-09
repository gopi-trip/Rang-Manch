from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select, func
from model import (ReviewCreate, ReviewRead, ReviewUpate, Review)
from database import get_session
from exceptions import (NoReviewsFound,NoReviewFound)

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

#Calculating the average rating
@router.get("/average/{play_name}")
def get_average_rating(play_name:str, session: Session = Depends(get_session)):
    result = session.exec(
        select(
            func.avg(Review.rating), 
            func.count(Review.id)
        ).where(Review.play_name == play_name)
    ).first()

    avg_rating,total_reviews = result

    if total_reviews == 0:
        raise NoReviewsFound(play_name=play_name) 

    return {
        "Play Name":play_name,
        "Average rating": round(avg_rating,2),
        "Total reviews": total_reviews
    }


@router.get("/{id}",response_model=ReviewRead)
def get_review_by_id(id:int, session: Session = Depends(get_session)):

    result = session.exec(
        select(
           Review.play_name,
           Review.reviewer_name,
           Review.created_at 
        ).where(Review.id == id)
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail={
                "Error":"No review corresponding to the id:{id}"
            }
        )

    play_name,revier_name,created_at = result

    return {
        "Play name":play_name,
        "Reviewer name":revier_name,
        "Review created at":created_at
    }


@router.patch("/{id}",response_model=ReviewRead)
def update_review_by_id(id:int, request: ReviewUpate,session: Session = Depends(get_session)):
    review = session.get(Review,id)

    if not review:
        raise NoReviewFound(id=id)

    update_data = request.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(review,key,value)

    session.add(review)
    session.commit()
    session.refresh(review)

    return review
       
@router.delete("/{id}")
def delete_review(id: int,session: Session = Depends(get_session)):
    review = session.get(Review,id)

    if not review:
        raise NoReviewFound(id=id)

    session.delete(review)
    session.commit()

    return {
        "Message":"The review with the ID: {id} has been deleted"
    }