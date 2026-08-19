from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import sqlalchemy_database_url


class Base(DeclarativeBase):
    pass


engine = create_engine(sqlalchemy_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
