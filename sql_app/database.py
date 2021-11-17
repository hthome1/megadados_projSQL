from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('SQL_APP_USER')
PASSWORD = os.getenv('SQL_APP_PASS')

SQLALCHEMY_DATABASE_URL = "mysql://"+USER+":"+PASSWORD+"@localhost/sql_app"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()