from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models.movie import Movie

from schemas.movie_schemas import (
    MovieCreate,
    MovieResponse
)


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get(
    "/",
    response_model=list[MovieResponse]
)
def get_movies(
    db: Session = Depends(get_db)
):

    movies = db.query(Movie).all()

    return movies

@router.get(
    "/{movie_id}",
    response_model=MovieResponse
)
def get_movie(
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

    return movie
    
@router.post(
    "/",
    response_model=MovieResponse
)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db)
):

    new_movie = Movie(

        title=movie.title,

        image=movie.image,

        rating=movie.rating,

        genre=movie.genre,

        duration=movie.duration,

        release_date=movie.release_date,

        language=movie.language,

        director=movie.director,

        cast=movie.cast,

        description=movie.description,

        trailer=movie.trailer,

        movie_type=movie.movie_type,

        refund_policy=movie.refund_policy,

        location=movie.location,

        theatre=movie.theatre

    )

    db.add(new_movie)

    db.commit()

    db.refresh(new_movie)

    return new_movie

@router.put(
    "/{movie_id}",
    response_model=MovieResponse
)
def update_movie(
    movie_id: int,
    movie: MovieCreate,
    db: Session = Depends(get_db)
):

    existing_movie = db.query(Movie).filter(
        Movie.id == movie_id
    ).first()

    if not existing_movie:

        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    existing_movie.title = movie.title

    existing_movie.image = movie.image

    existing_movie.rating = movie.rating

    existing_movie.genre = movie.genre

    existing_movie.duration = movie.duration

    existing_movie.release_date = movie.release_date

    existing_movie.language = movie.language

    existing_movie.director = movie.director

    existing_movie.cast = movie.cast

    existing_movie.description = movie.description

    existing_movie.trailer = movie.trailer

    existing_movie.movie_type = movie.movie_type

    existing_movie.refund_policy = movie.refund_policy

    existing_movie.location = movie.location

    existing_movie.theatre = movie.theatre

    db.commit()

    db.refresh(existing_movie)

    return existing_movie

@router.delete(
    "/{movie_id}"
)
def delete_movie(
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

    try:

        db.delete(movie)

        db.commit()

        return {
            "message":
                "Movie deleted successfully"
        }

    except Exception:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=
                "Movie cannot be deleted because it is used in bookings"
        )
