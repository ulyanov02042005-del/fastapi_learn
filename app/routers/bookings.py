from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status
from fastapi.encoders import jsonable_encoder

from ..database import fake_bookings_db, fake_spaces_db
from ..dependencies import UserInDB, get_current_user
from ..exceptions import SpaceNotFoundError
from ..schemas import Booking

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("/space/{space_id}")
async def booking(space_id: Annotated[
                                    int, 
                                    Path(gt=0)], hours: int,
                                    user: Annotated[UserInDB, Depends(get_current_user)] 
                                    ):
    if space_id not in fake_spaces_db:
        raise SpaceNotFoundError(space=space_id)
    username = user.username
    total_cost = fake_spaces_db[space_id]["price_per_hour"] * hours
    current_booking_length = max(fake_bookings_db.keys(), default=0) + 1
    booking = {
        "booking_id": current_booking_length,
        "space_id": space_id,
        "username": username,
        "hours": hours,
        "total_cost": total_cost
    }
    fake_bookings_db[current_booking_length] = booking
    return booking

router.patch("/{booking_id}")
async def change_booking(booking_id: int,
                         user: Annotated[UserInDB, Depends(get_current_user)],
                        booking: Booking
                         ):
    if booking_id not in fake_bookings_db:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    if user.username != fake_bookings_db[booking_id]["username"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    booking_from_db = fake_bookings_db[booking_id]
    from_db_model = Booking(**booking_from_db)
    values_to_change = booking.model_dump(exclude_unset=True)
    booking_updated = from_db_model.model_copy(update=values_to_change)
    booking_updated.total_cost = booking_updated.hours*fake_spaces_db[booking_updated.space_id]["price_per_hour"]
    fake_bookings_db[booking_id] = jsonable_encoder(booking_updated)
    return booking_updated