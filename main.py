from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel
from db.db import engine
from endpoints.gem_endpoints import gem_router
from endpoints.user_endpoints import user_router

app = FastAPI()

app.include_router(gem_router)
app.include_router(user_router)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
create_db_and_tables()

@app.get("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)