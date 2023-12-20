from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator 
from core.config import settings
from sqlalchemy.engine.url import URL 
# import cx_Oracle
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# connect_url = URL(
#     "oracle+cx_oracle",
#     username = "INTELLECT",
#     password = "Db51411#",
#     host = "172.16.0.40",
#     port = 1521,
#     database = "ORCL"
# )
# connect_url = cx_Oracle.connect("INTELLECT/Db51411#/172.16.0.40:1521/orcl")
# engine = create_engine(connect_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()