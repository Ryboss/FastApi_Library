import datetime

from sqlalchemy import sql, Column, String, Integer, ForeignKey, DateTime, Boolean, BigInteger, Text
from sqlalchemy.orm import relationship
from passlib import hash

from database import Base


class User(Base):
    __tablename__ = "Users"
    id = Column("id", Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column("Имя", String, unique=False,nullable=False)
    last_name = Column("Фамилия", String, unique=False, nullable=False)
    middle_name = Column("Отчество", String, unique=False, nullable=True)
    phone = Column("Телефон", BigInteger, unique=False, nullable=True)
    company_id = Column("Компания", Integer, unique=False, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, unique=False, nullable=True)
    hashed_password = Column(String, nullable=True, unique=False)

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)


class Work(Base):
    __tablename__ = "Work"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name_company = Column("Название компании",String, unique=False, nullable=True)
    company_description = Column("Описание компании", Text, unique=False, nullable=True)
    name_vacancy = Column("Название вакансии", String, unique=False, nullable=False)
    vacance_description = Column("Описание вакансии", Text, unique=False, nullable=False)
    salary_from = Column("Зарплата от", BigInteger, unique=False)
    salary_up_to = Column("Зарплта до", BigInteger, unique=False, nullable=True)

class Roles(Base):
    __tablename__ = "Roles"
    id = Column("id", Integer, primary_key=True, autoincrement=True, unique=True)
    role_name = Column("Название роли", String, unique=True, nullable=False)
    role_alias = Column("Название роли на английском", String, unique=True, nullable=False)