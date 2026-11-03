from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from models.movie_theatre import MovieTheatre
from models.movie import Movie
from models.theatre import Theatre


router = APIRouter(
    prefix="/movie-theatres",
    tags=["Movie Theatres"]
)


@router.post("/")
def add_movie_to_theatre(
    movie_id: int,
    theatre_id: int,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    theatre = db.query(Theatre).filter(
        Theatre.id == theatre_id
    ).first()

    if not theatre:
        raise HTTPException(
            status_code=404,
            detail="Theatre not found"
        )

    existing = db.query(MovieTheatre).filter(
        MovieTheatre.movie_id == movie_id,
        MovieTheatre.theatre_id == theatre_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Movie already assigned to this theatre"
        )

    movie_theatre = MovieTheatre(
        movie_id=movie_id,
        theatre_id=theatre_id
    )

    db.add(movie_theatre)
    db.commit()
    db.refresh(movie_theatre)

    return movie_theatre


@router.get("/movie/{movie_id}")
def get_movie_theatres(
    movie_id: int,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    results = (
        db.query(
            MovieTheatre,
            Theatre
        )
        .join(
            Theatre,
            MovieTheatre.theatre_id == Theatre.id
        )
        .filter(
            MovieTheatre.movie_id == movie_id
        )
        .all()
    )

    return [
        {
            "id": movie_theatre.id,
            "movie_id": movie_theatre.movie_id,
            "theatre_id": theatre.id,
            "theatre_name": theatre.name,
            "location_id": theatre.location_id,
            "city": theatre.city,
            "area": theatre.area,
            "address": theatre.address,
            "screens": theatre.screens
        }
        for movie_theatre, theatre in results
    ]


@router.get("/theatre/{theatre_id}")
def get_theatre_movies(
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

    results = (
        db.query(
            MovieTheatre,
            Movie
        )
        .join(
            Movie,
            MovieTheatre.movie_id == Movie.id
        )
        .filter(
            MovieTheatre.theatre_id == theatre_id
        )
        .all()
    )

    return [
        {
            "id": movie_theatre.id,
            "movie_id": movie.id,
            "title": movie.title
        }
        for movie_theatre, movie in results
    ]


@router.delete("/{movie_theatre_id}")
def delete_movie_from_theatre(
    movie_theatre_id: int,
    db: Session = Depends(get_db)
):

    movie_theatre = db.query(MovieTheatre).filter(
        MovieTheatre.id == movie_theatre_id
    ).first()

    if not movie_theatre:
        raise HTTPException(
            status_code=404,
            detail="Movie theatre assignment not found"
        )

    db.delete(movie_theatre)
    db.commit()

    return {
        "message": "Movie removed from theatre successfully"
    }
