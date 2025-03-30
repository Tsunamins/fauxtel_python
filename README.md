# Fauxtel Python

An alternative backend to my personal project Fauxtel Hotels, in Python/FastAPI.

A work in progress, eventually meant to be synced with my FauxtelHotels frontend and have a more user frienly instructions for running locally.

To run, I recommend creating a local docker container in postgres or setup postgres locally. Eventually I'll do a Docker file.

You will need to create a database.py file under the app directory with the following
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = <yourdatabaseinfohere>


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()

From here uvicorn app.main:app --reload should do the trick.

Fauxtel docs will be at: http://localhost:8000/docs