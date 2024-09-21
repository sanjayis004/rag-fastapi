from fastapi import FastAPI
from app.routers import question_router

app = FastAPI()

app.include_router(question_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Question Answering Service!"}
