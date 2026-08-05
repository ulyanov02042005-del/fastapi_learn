from fastapi import FastAPI

# Имя переменной должно быть строго 'app'
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "FastAPI работает в WSL!"}
