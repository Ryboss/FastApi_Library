import datetime
from typing import Optional, Dict, List


from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str]
    phone: Optional[int]
    company_id: Optional[int]
    role : Optional[int]
    email: str




class UserCreate(UserBase):
    hashed_password: str
    username: str
    class Config:
        schema_extra = {
            "example": {
                "username": "TestName",
                "first_name": "FirstTest",
                "last_name": "LastName",
                "middle_name": "MiddleName",
                "email": "test@mail.ru",
                "phone": 79001234567,
                "company_id": 0,
                "role": 0,
                "hashed_password": "string"
            },
        }


class User(UserBase):
    id: int
    role: str
    class Config:
        orm_mode = True

class WorkBase(BaseModel):

    name_company: str
    company_description: str
    name_vacancy: str
    vacance_description: str
    salary_from: int
    salary_up_to: int

    class Config:
        schema_extra = {
            "example":
                {
                    "name_company": "Test_company",
                    "company_description": "test_description",
                    "name_vacancy": "test_name",
                    "vacance_description": "test_description",
                    "salary_from": 0,
                    "salary_up_to": 0
                }
        }


class RoleBase(BaseModel):
    role_name: str
    role_alias: str

    class Config:
        schema_extra={
            "example":{
                "role_name": "test role",
                "role_alias": "test_role_in_english"
            }
        }