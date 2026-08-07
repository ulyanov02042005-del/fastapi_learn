from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.post("/flights/search")
async def read_items(
    airport_code: Annotated[
        str, 
        Query(
            min_length=3, 
            max_length=3,
            alias="from-airport",
            description="Код аэропорта вылета (3 символа)"
        )
    ], 
    # 1. Добавили = None в самый конец, чтобы параметр стал необязательным
    airline: Annotated[
        str | None, 
        Query(
            min_length=2,
            description="Название авиакомпании для фильтрации"
        )
    ] = None 
# 2. Четко указали, что функция возвращает dict, где значения могут быть str или None
) -> dict[str, str | None]:
    
    results: dict[str, str | None] = {"status": "searching", "airport": airport_code}
    
    if airline:
        results.update({"airline": airline})
        
    return results
