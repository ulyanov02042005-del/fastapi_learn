from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class NotEnoughPermissionsError(Exception):
    def __init__(self) -> None:
        pass

class SpaceNotFoundError(Exception):
    def __init__(self, space: str) -> None:
        self.space = space
        

def register_exceptions(app: FastAPI):
    @app.exception_handler(NotEnoughPermissionsError)
    async def no_permission_handler(request: Request, exc: NotEnoughPermissionsError):
        return JSONResponse(
            status_code=403,
            content={
                "status": "error", 
                "reason": "Требуются права администратора."}
        )

    @app.exception_handler(SpaceNotFoundError)
    async def no_space_handler(request: Request, exc: SpaceNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "status": "error", 
                "reason": f"Зона {exc.space} не была найдена."}
        )