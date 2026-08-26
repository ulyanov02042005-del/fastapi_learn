from exceptions import register_exceptions
from fastapi import FastAPI
from routers import auth, bookings, spaces

app = FastAPI(
    title="Space Booking API",
    description="API для бронирования пространств и зон",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(spaces.router)

register_exceptions(app)

@app.get("/")
async def root():
    pass