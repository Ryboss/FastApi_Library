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

roles = ('admin', 'librarian')

#Users
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

@app.put('/api/user/{user_id}', response_model=User, status_code=fastapi.status.HTTP_200_OK)
def update_an_item(user_id: int, user1: User, user: models.User= fastapi.Depends(services.get_current_user)):
    # if user.role not in roles:
    #     raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    user_role_update = db.query(models.User).filter(models.User.id == user_id).first()
    user_role_update.role = user1.role

    db.commit()

    return user_role_update

#Books
@app.get('/books', response_model=List[Book], status_code=200)
def get_all_items():
    items = db.query(models.Book).all()
    return items


@app.get('/books/{books_id}', response_model=Book, status_code=fastapi.status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Book).filter(models.Book.id == item_id).first()
    return item


@app.post('/books', response_model=Book,
          status_code=fastapi.status.HTTP_201_CREATED)
def create_an_item(item: Book,
                   user: schemas.User = fastapi.Depends(services.get_current_user)):
    if user.role not in roles:
        raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
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

@app.post('/booking/create')
def booking_create(booking:Booking, user: schemas.User = fastapi.Depends(services.get_current_user)):
    new_booking = models.Booking(
        book_title=booking.book_title,
        user_email=user.email,
    )
    db_book = db.query(models.Book).filter(models.Book.title == booking.book_title).first()

    print(db_book.in_stock)
    if not db_book or db_book.in_stock == False:
        raise fastapi.HTTPException(status_code=401, detail=f"We havent book {booking.book_title} or book booked")
    db_book.in_stock = False
    db.add(new_booking)
    db.commit()

    return f"Successfull booking {new_booking.book_title} create"


@app.put('/books/{book_id}', response_model=Book, status_code=fastapi.status.HTTP_200_OK)
def update_an_item(item_id: int, item: Book, user: models.User= fastapi.Depends(services.get_current_user)):
    if user.role not in roles:
        raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    item_to_update = db.query(models.Book).filter(models.Book.id == item_id).first()
    item_to_update.title = item.title
    item_to_update.author = item.author
    item_to_update.pages = item.pages
    item_to_update.in_stock = item.in_stock

    db.commit()

    return item_to_update


@app.delete('/book/{book_id}')
def delete_item(item_id: int,
                user: models.User= fastapi.Depends(services.get_current_user)):
    item_to_delete = db.query(models.Book).filter(models.Book.id == item_id).first()
    if user.role not in roles:
        raise fastapi.HTTPException(status_code=401, detail=f"Your role is not included in {roles}")
    if item_to_delete is None:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete
