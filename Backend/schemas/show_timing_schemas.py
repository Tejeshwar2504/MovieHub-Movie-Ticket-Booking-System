from pydantic import BaseModel

class ShowTimingCreate(BaseModel):

    movie_id: int

    theatre_id: int

    language: str

    show_time: str

    price: int

class ShowTimingResponse(BaseModel):

    id: int

    movie_id: int

    theatre_id: int

    language: str

    show_time: str

    price: int

    class Config:

        from_attributes = True
