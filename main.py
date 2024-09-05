from fastapi import FastAPI
from app.routers import location, room



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(location.router)
app.include_router(room.router)