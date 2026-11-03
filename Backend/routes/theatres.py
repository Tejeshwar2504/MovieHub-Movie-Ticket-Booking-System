from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models.theatre import Theatre

from schemas.theatre_schemas import (
    TheatreCreate,
    TheatreResponse
)


router = APIRouter(
    prefix="/theatres",
    tags=["Theatres"]
)

@router.get(
    "/",
    response_model=list[TheatreResponse]
)
def get_theatres(
    db: Session = Depends(get_db)
):

    return db.query(Theatre).all()

@router.get("/location/{location_id}")
def get_theatres_by_location(
    location_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Theatre).filter(
        Theatre.location_id == location_id
    ).all()

@router.post(
    "/",
    response_model=TheatreResponse
)
def create_theatre(
    theatre: TheatreCreate,
    db: Session = Depends(get_db)
):

    new_theatre = Theatre(
        name=theatre.name,
        location_id=theatre.location_id,
        city=theatre.city,
        area=theatre.area,
        address=theatre.address,
        screens=theatre.screens
    )

    db.add(new_theatre)
    db.commit()
    db.refresh(new_theatre)

    return new_theatre

@router.delete("/{theatre_id}")
def delete_theatre(
    theatre_id: int,
    db: Session = Depends(get_db)
):

    theatre = db.query(Theatre).filter(
        Theatre.id == theatre_id
    ).first()

    if not theatre:
        raise HTTPException(
            status_code=404,
            detail="Theatre not found"
        )

    db.delete(theatre)
    db.commit()

    return {
        "message": "Theatre deleted successfully"
    }

@router.delete("/admin/delete-all")
def delete_all_theatres(
    db: Session = Depends(get_db)
):

    theatres = db.query(Theatre).all()

    count = len(theatres)

    for theatre in theatres:

        db.delete(theatre)

    db.commit()

    return {

        "message":
            "All theatres deleted successfully",

        "deleted_count":
            count

    }
