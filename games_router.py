from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from pydantic import Field, BaseModel

def audit_logger():
    print("[Audit] Зафиксировано обращение к каталогу игр")

async def verify_partner_token(partner_token: str):
    if partner_token != "dev-partner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Доступ запрещен: вы не являетесь сертифицированным партнером"
        )
    return partner_token

async def get_db(valid_token: Annotated[str, Depends(verify_partner_token)]):
    print("[Database] Пул подключений инициализирован")
    try:
        yield { "status": "connected", "engine": "postgresql" }
    finally:
        print("[Database] Соединение безопасно возвращено в пул")

class ActivationKey(BaseModel):
    key_code: str = Field(..., pattern=r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$")
    is_used: bool = False

class GameBase(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0, le=5000)

class GameCreate(GameBase):
    keys: list[ActivationKey] = Field(min_length=1)

class GameResponse(GameBase):
    id: int
    available_keys_count: int

router = APIRouter(
    dependencies=[Depends(audit_logger)],
    prefix="/games",
    tags=["Игры"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def Gamecreate(game: GameCreate,
                     db: Annotated[str, Depends(get_db)]) -> GameResponse:
    count = 0
    for key in game.keys:
        if key.is_used==False:
            count += 1
    return GameResponse(
        id = 777,
        available_keys_count=count,
        title = game.title,
        price=game.price
    )

@router.get("/{game_id}")
async def get_info(game_id: Annotated[int, Path(gt=0, le=9999)],
                   detailed: bool = False):
    if game_id!=777:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Игра не найдена в каталоге"
        )
    return GameResponse(
            id = 777,
            available_keys_count=2,
            title = "fwfwf",
            price= 200.0
        )