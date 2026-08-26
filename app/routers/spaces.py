from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..database import fake_spaces_db
from ..dependencies import get_admin_user
from ..schemas import Space

router = APIRouter(
    prefix="/spaces",
    tags=["Spaces"]
)

@router.post("/", dependencies=[Depends(get_admin_user)])
async def create_space(space: Space):
    space_for_db = space.model_dump()
    space_id = space_for_db["space_id"]
    fake_spaces_db[space_id] = space_for_db
    return space_for_db

@router.get("/")
async def get_spaces(
    space_type:str | None = None, 
    max_price: Annotated[int|None, Query(gt=0)]=None
    ):
    found_spaces: list[Space] = []
    for space in fake_spaces_db.values():
        match_type = (space_type is None) or (space["type"] == space_type)
        match_price = (max_price is None) or (space["price_per_hour"] <= max_price)
        if match_price and match_type:
            found_spaces.append(space)
    return found_spaces