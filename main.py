from fastapi import FastAPI
from app.routers import location, room, reservation, user, auth_google



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(location.router)
app.include_router(room.router)
app.include_router(reservation.router)
app.include_router(user.router)
app.include_router(auth_google.router)
