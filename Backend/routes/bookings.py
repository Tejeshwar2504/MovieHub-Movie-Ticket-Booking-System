from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from database import get_db

from models.booking import Booking
from models.movie import Movie

from schemas.booking import (
    BookingCreate,
    BookingResponse
)


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post(
    "/",
    response_model=BookingResponse
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.id == booking.movie_id
    ).first()


    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    refund_policy = (
        movie.refund_policy
        if movie.refund_policy
        else "refundable"
    )

    existing_bookings = db.query(Booking).filter(

        Booking.movie_id == booking.movie_id,

        Booking.date == booking.date,

        Booking.time == booking.time,

        Booking.theatre == booking.theatre,

        Booking.status == "confirmed"

    ).all()

    booked_seats = []


    for existing_booking in existing_bookings:

        if existing_booking.seats:

            booked_seats.extend(
                existing_booking.seats
            )

    requested_seats = booking.seats or []

    already_booked = []

    for seat in requested_seats:

        if seat in booked_seats:

            already_booked.append(seat)
            
    already_booked = list(
        dict.fromkeys(already_booked)
    )

    if already_booked:

        raise HTTPException(

            status_code=400,

            detail=(
                "Seat(s) already booked: "
                + ", ".join(already_booked)
            )

        )

    if not requested_seats:

        raise HTTPException(

            status_code=400,

            detail="Please select at least one seat"

        )

    new_booking = Booking(

        booking_id=
            "MH" +
            str(uuid.uuid4())[:8],

        user_id=
            booking.user_id,

        movie_id=
            booking.movie_id,

        movie=
            booking.movie,

        image=
            booking.image,

        city=
            booking.city,

        theatre=
            booking.theatre,

        date=
            booking.date,

        time=
            booking.time,

        seats=
            requested_seats,

        price=
            booking.price,
        
        refund_policy=
            refund_policy,

        status=
            "confirmed"

    )

    db.add(
        new_booking
    )

    db.commit()

    db.refresh(
        new_booking
    )


    return new_booking


@router.get(
    "/",
    response_model=list[BookingResponse]
)
def get_bookings(
    db: Session = Depends(get_db)
):

    return db.query(
        Booking
    ).all()


@router.get(
    "/user/{user_id}",
    response_model=list[BookingResponse]
)
def get_user_bookings(
    user_id: int,
    db: Session = Depends(get_db)
):

    return db.query(
        Booking
    ).filter(

        Booking.user_id == user_id,

        Booking.status == "confirmed"

    ).all()

@router.put(
    "/cancel/{booking_id}"
)
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db)
):

    booking = db.query(
        Booking
    ).filter(

        Booking.booking_id == booking_id

    ).first()


    if not booking:

        raise HTTPException(

            status_code=404,

            detail="Booking not found"

        )

    if booking.status == "cancelled":

        raise HTTPException(

            status_code=400,

            detail="Booking is already cancelled"

        )

    if (

        booking.refund_policy and

        booking.refund_policy.lower()
        == "non_refundable"

    ):

        raise HTTPException(

            status_code=400,

            detail=(
                "This booking is non-refundable "
                "and cannot be cancelled"
            )

        )

    booking.status = "cancelled"


    db.commit()

    db.refresh(
        booking
    )


    return {

        "message":
            "Booking cancelled successfully",

        "booking_id":
            booking.booking_id,

        "status":
            booking.status

    }

@router.get(
    "/booked-seats/{movie_id}/{date}/{time}/{theatre}"
)
def get_booked_seats(

    movie_id: int,

    date: str,

    time: str,

    theatre: str,

    db: Session = Depends(get_db)

):

    bookings = db.query(
        Booking
    ).filter(

        Booking.movie_id == movie_id,

        Booking.date == date,

        Booking.time == time,

        Booking.theatre == theatre,

        Booking.status == "confirmed"

    ).all()

    booked_seats = []

    for booking in bookings:

        if booking.seats:

            booked_seats.extend(
                booking.seats
            )

    return {

        "booked_seats":
            booked_seats

    }
