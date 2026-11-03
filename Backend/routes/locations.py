from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.theatre import Theatre
from models.show_timing import ShowTiming
from database import get_db
from models.location import Location

from schemas.location_schemas import (
    LocationCreate,
    LocationResponse
)


router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)

@router.get(
    "/",
    response_model=list[LocationResponse]
)
def get_locations(
    db: Session = Depends(get_db)
):

    locations = (
        db.query(Location)
        .order_by(
            Location.city,
            Location.id
        )
        .all()
    )

    grouped_locations = {}


    for location in locations:

        city = location.city


        if city not in grouped_locations:

            grouped_locations[city] = {

                "id": location.id,

                "city": city,

                "area": []

            }


        grouped_locations[city]["area"].append({

            "id": location.id,

            "name": location.area

        })


    return list(
        grouped_locations.values()
    )


@router.post(
    "/",
    response_model=dict
)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db)
):


    existing_location = db.query(Location).filter(

        Location.city == location.city,

        Location.area == location.area

    ).first()


    if existing_location:

        raise HTTPException(

            status_code=400,

            detail=(
                f"{location.area} already exists "
                f"in {location.city}"
            )

        )

    new_location = Location(

        city=location.city,

        area=location.area,

        state=location.state

    )


    db.add(new_location)

    db.commit()

    db.refresh(new_location)


    return {

        "message":
            "Location created successfully",

        "location": {

            "id":
                new_location.id,

            "city":
                new_location.city,

            "area": {

                "id":
                    new_location.id,

                "name":
                    new_location.area

            },

            "state":
                new_location.state

        }

    }

@router.delete(
    "/{location_id}"
)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db)
):

    location = db.query(Location).filter(

        Location.id == location_id

    ).first()


    if not location:

        raise HTTPException(

            status_code=404,

            detail="Location not found"

        )


    db.delete(location)

    db.commit()


    return {

        "message":
            "Location deleted successfully"

    }
    
@router.delete("/admin/delete-all")
def delete_all_locations(
    db: Session = Depends(get_db)
):

    show_timings_count = db.query(
        ShowTiming
    ).count()


    db.query(
        ShowTiming
    ).delete(
        synchronize_session=False
    )

    theatres_count = db.query(
        Theatre
    ).count()


    db.query(
        Theatre
    ).delete(
        synchronize_session=False
    )

    locations_count = db.query(
        Location
    ).count()


    db.query(
        Location
    ).delete(
        synchronize_session=False
    )

    db.commit()


    return {

        "message":
            "All locations, theatres and show timings deleted successfully",

        "locations_deleted":
            locations_count,

        "theatres_deleted":
            theatres_count,

        "show_timings_deleted":
            show_timings_count

    }
