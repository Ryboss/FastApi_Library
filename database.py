import sqlalchemy as _sql
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as _orm

DATABASE_URL = "postgresql://postgres:admin@localhost/diplom2"

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
