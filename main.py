from typing import List
import fastapi as fastapi
import fastapi.security as security


import models
from schemas import *
import sqlalchemy.orm as _orm
from database import SessionLocal
import services
import schemas


app = fastapi.FastAPI(title="Система для \n высших образовательных учреждений",
                      description="Система позволяющая размещать вакансии на работу на сайте  университета")

db=SessionLocal()

roles = ('admin', 'librarian')


# Пользователи

@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate, db: _orm.Session = fastapi.Depends(services.get_db)
):
    """
    Создание пользователя
    """

    db_user = await services.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await services.create_user(user, db)

    return await services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: security.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: _orm.Session = fastapi.Depends(services.get_db),
):

    user = await services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await services.create_token(user)


@app.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    """Получение авторизированного пользователя"""

    return user


@app.put('/api/user/{user_id}', response_model=User, status_code=fastapi.status.HTTP_200_OK)
def update_user(user_id: int, user1: User, user: models.User= fastapi.Depends(services.get_current_user)):
    """
    Обновление пользователя
    """
    # if user.role not in roles:
    #     raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    user_role_update = db.query(models.User).filter(models.User.id == user_id).first()
    user_role_update.role = user1.role

    db.commit()

    return user_role_update

# Роли пользователей
@app.get('/api/all_roles', response_model=List[RoleBase], status_code=200)
async def all_roles():

    query = db.query(models.Roles).all()
    print(List[query])
    return query

@app.post('/api/add_role')
async def create_role(item: RoleBase):
    new_item = models.Roles(
        role_name=item.role_name,
        role_alias=item.role_alias
    )

    db.add(new_item)
    db.commit()

    return new_item
# Вакансии
@app.get('/vacancy', response_model=List[WorkBase], status_code=200)
async def get_all_items():
    """Получение всех вакансий"""

    items = db.query(models.Work).all()
    return items


@app.get('/vacancy/{vacancy_id}', response_model=WorkBase, status_code=fastapi.status.HTTP_200_OK)
async def get_an_item(item_id: int):
    """Получение вакансии по id"""

    item = db.query(models.Work).filter(models.Work.id == item_id).first()
    return item


@app.post('/vacancy', response_model=WorkBase,
          status_code=fastapi.status.HTTP_201_CREATED)
async def create_item(item: WorkBase,
                   user: schemas.User = fastapi.Depends(services.get_current_user)):
    """
    Создание вакансии
    """
    # if user.role not in roles:
    #     raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    # db_item = db.query(models.Work).filter(models.Work.title == item.title).first()

    # if db_item is not None:
    #     raise fastapi.HTTPException(status_code=400, detail="Item already exists")

    new_item = models.Work(

        name_company=item.name_company,
        company_description=item.company_description,
        name_vacancy=item.name_vacancy,
        vacance_description=item.vacance_description,
        salary_from=item.salary_from,
        salary_up_to=item.salary_up_to,
    )

    db.add(new_item)
    db.commit()

    return new_item



@app.put('/vacancy/{vacancy_id}', response_model=WorkBase, status_code=fastapi.status.HTTP_200_OK)
async def update_item(item_id: int, item: WorkBase, user: models.User= fastapi.Depends(services.get_current_user)):
    """
    Обновление вакансии 
    """

    if user.role not in roles:
        raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    item_to_update = db.query(models.Work).filter(models.Work.id == item_id).first()
    item_to_update.name_company = item.name_company
    item_to_update.company_description = item.company_description
    item_to_update.name_vacancy = item.name_vacancy
    item_to_update.vacance_description = item.vacance_description
    item_to_update.salary_from = item.salary_from
    item_to_update.salary_up_to = item.salary_up_to

    db.commit()

    return item_to_update


@app.delete('/vacancy/{vacancy_id}')
async def delete_item(item_id: int,
                user: models.User= fastapi.Depends(services.get_current_user)):
    """
    Удаление вакансии
    """

    item_to_delete = db.query(models.Work).filter(models.Work.id == item_id).first()

    if user.role not in roles:
        raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    if item_to_delete is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete
