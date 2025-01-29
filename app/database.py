from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
from psycopg2.extras import RealDictCursor

from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#для себя, из туториала


# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', 
#         password='holera1211', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succsessful')
#         break
#     except Exception as error:
#         print("Connection to the database is failed")   
#         print("Error: ", error) 
#         time.sleep(2)