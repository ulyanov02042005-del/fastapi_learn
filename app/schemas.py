from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
    username: str
    email: str
    role: str | None = Field(default="client")

class UserCreate(User):
    password: str = Field(min_length=6)

class UserInDB(User):
    hashed_password: str

class Space(BaseModel):
    space_id: int
    name: str = Field(min_length=3, max_length=50)
    type: Literal["open-space", "meeting-room"]
    price_per_hour: int = Field(gt=0)
    amenities: list[str] | None = None

class Booking(BaseModel):
    booking_id: str
    space_id: int
    username: str
    hours: int = Field(ge=1, le=8)
    total_cost: int