from typing import List
import fastapi as fastapi
import fastapi.security as security
import models
from schemas import *
import sqlalchemy.orm as _orm
from database import SessionLocal
import services
import schemas

app = fastapi.FastAPI()

db=SessionLocal()

@app.post("/api/users")
async def create_user(
    user: schemas.UserCreate, db: _orm.Session = fastapi.Depends(services.get_db)
):
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
    return user


@app.get('/books', response_model=List[Book], status_code=200)
def get_all_items():
    items = db.query(models.Item).all()
    return items


@app.get('/books/{books_id}', response_model=Book, status_code=fastapi.status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


@app.post('/books', response_model=Book,
          status_code=fastapi.status.HTTP_201_CREATED)
def create_an_item(item: Book):
    db_item = db.query(models.Book).filter(models.Book.title == item.title).first()

    if db_item is not None:
        raise fastapi.HTTPException(status_code=400, detail="Item already exists")

    new_item = models.Book(
        title=item.title,
        author=item.author,
        pages=item.pages,
        in_stock=item.in_stock
    )

    db.add(new_item)
    db.commit()

    return new_item


@app.put('/books/{book_id}', response_model=Book, status_code=fastapi.status.HTTP_200_OK)
def update_an_item(item_id: int, item: Book):
    item_to_update = db.query(models.Book).filter(models.Book.id == item_id).first()
    item_to_update.title = item.title
    item_to_update.author = item.author
    item_to_update.pages = item.pages
    item_to_update.in_stock = item.in_stock

    db.commit()

    return item_to_update


@app.delete('/book/{book_id}')
def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_delete is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete