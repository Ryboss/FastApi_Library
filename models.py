import datetime

from sqlalchemy import sql, Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from passlib import hash

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String,unique=False, default='user')
    hashed_password = Column(String)

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)


class Book(Base):
    __tablename__ = "Books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    pages = Column(Integer)
    in_stock=Column(Boolean, default=False)
    date_created = Column(DateTime)
    date_last_updated = Column(DateTime, default=datetime.datetime.utcnow)
