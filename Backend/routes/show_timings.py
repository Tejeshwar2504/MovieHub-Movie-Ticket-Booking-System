from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models.show_timing import ShowTiming

from schemas.show_timing_schemas import (
    ShowTimingCreate,
    ShowTimingResponse
)


router = APIRouter(
    prefix="/show-timings",
    tags=["Show Timings"]
)

@router.get(
    "/",
    response_model=list[ShowTimingResponse]
)
def get_show_timings(
    db: Session = Depends(get_db)
):

    return db.query(
        ShowTiming
    ).all()

@router.post(
    "/",
    response_model=ShowTimingResponse
)
def create_show_timing(
    timing: ShowTimingCreate,
    db: Session = Depends(get_db)
):

    allowed_languages = [
        "Tamil",
        "Telugu",
        "Malayalam",
        "Hindi",
        "English"
    ]

    if timing.language not in allowed_languages:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid language. "
                "Allowed languages are: "
                "Tamil, Telugu, Malayalam, Hindi, English."
            )
        )

    if timing.price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Ticket price must be greater than 0."
        )

    if not timing.show_time.strip():

        raise HTTPException(
            status_code=400,
            detail="Show time is required."
        )

    existing = db.query(
        ShowTiming
    ).filter(
        ShowTiming.movie_id == timing.movie_id,
        ShowTiming.theatre_id == timing.theatre_id,
        ShowTiming.language == timing.language,
        ShowTiming.show_time == timing.show_time
    ).first()


    if existing:

        raise HTTPException(
            status_code=400,
            detail=(
                "This show timing already exists "
                "for this movie, theatre, language "
                "and show time."
            )
        )
        
    new_timing = ShowTiming(

        movie_id=timing.movie_id,

        theatre_id=timing.theatre_id,

        language=timing.language,

        show_time=timing.show_time,

        price=timing.price

    )


    db.add(new_timing)

    db.commit()

    db.refresh(new_timing)


    return new_timing

@router.put(
    "/{timing_id}",
    response_model=ShowTimingResponse
)
def update_show_timing(
    timing_id: int,
    timing: ShowTimingCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(
        ShowTiming
    ).filter(
        ShowTiming.id == timing_id
    ).first()


    if not existing:

        raise HTTPException(
            status_code=404,
            detail="Show timing not found"
        )

    allowed_languages = [
        "Tamil",
        "Telugu",
        "Malayalam",
        "Hindi",
        "English"
    ]

    if timing.language not in allowed_languages:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid language. "
                "Allowed languages are: "
                "Tamil, Telugu, Malayalam, Hindi, English."
            )
        )

    if timing.price <= 0:

        raise HTTPException(
            status_code=400,
            detail="Ticket price must be greater than 0."
        )

    if not timing.show_time.strip():

        raise HTTPException(
            status_code=400,
            detail="Show time is required."
        )

    duplicate = db.query(
        ShowTiming
    ).filter(
        ShowTiming.id != timing_id,
        ShowTiming.movie_id == timing.movie_id,
        ShowTiming.theatre_id == timing.theatre_id,
        ShowTiming.language == timing.language,
        ShowTiming.show_time == timing.show_time
    ).first()


    if duplicate:

        raise HTTPException(
            status_code=400,
            detail=(
                "This show timing already exists "
                "for this movie, theatre, language "
                "and show time."
            )
        )

    existing.movie_id = timing.movie_id

    existing.theatre_id = timing.theatre_id

    existing.language = timing.language

    existing.show_time = timing.show_time

    existing.price = timing.price


    db.commit()

    db.refresh(existing)


    return existing

@router.get(
    "/movie/{movie_id}/theatre/{theatre_id}",
    response_model=list[ShowTimingResponse]
)
def get_movie_theatre_timings(
    movie_id: int,
    theatre_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        ShowTiming
    ).filter(
        ShowTiming.movie_id == movie_id,
        ShowTiming.theatre_id == theatre_id
    ).all()

@router.get(
    "/movie/{movie_id}",
    response_model=list[ShowTimingResponse]
)
def get_movie_timings(
    movie_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        ShowTiming
    ).filter(
        ShowTiming.movie_id == movie_id
    ).all()

@router.get(
    "/movie/{movie_id}/language/{language}",
    response_model=list[ShowTimingResponse]
)
def get_movie_language_timings(
    movie_id: int,
    language: str,
    db: Session = Depends(get_db)
):

    return db.query(
        ShowTiming
    ).filter(
        ShowTiming.movie_id == movie_id,
        ShowTiming.language == language
    ).all()

@router.get(
    "/movie/{movie_id}/theatre/{theatre_id}/language/{language}",
    response_model=list[ShowTimingResponse]
)
def get_movie_theatre_language_timings(
    movie_id: int,
    theatre_id: int,
    language: str,
    db: Session = Depends(get_db)
):

    return db.query(
        ShowTiming
    ).filter(
        ShowTiming.movie_id == movie_id,
        ShowTiming.theatre_id == theatre_id,
        ShowTiming.language == language
    ).all()
    
@router.delete(
    "/{timing_id}"
)
def delete_show_timing(
    timing_id: int,
    db: Session = Depends(get_db)
):

    timing = db.query(
        ShowTiming
    ).filter(
        ShowTiming.id == timing_id
    ).first()


    if not timing:

        raise HTTPException(
            status_code=404,
            detail="Show timing not found"
        )


    db.delete(timing)

    db.commit()


    return {
        "message": "Show timing deleted successfully"
    }
