import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    role : str
    email: str



class UserCreate(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    role: str
    class Config:
        orm_mode = True


class Book(BaseModel):
    title: str
    author: str
    pages: int
    in_stock: bool

    class Config:
        orm_mode = True



class Booking(BaseModel):
    id:int
    book_title:str


    class Config:
        orm_mode = True