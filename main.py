from fastapi import FastAPI
from app.routers import location, room, reservation, user, auth_google


app = FastAPI(title="Fauxtel API", description="API for managing reservations, rooms, and users", version="1.0.0")

app.include_router(location.router)
app.include_router(room.router)
app.include_router(reservation.router)
app.include_router(user.router)
app.include_router(auth_google.router)
