from backend.routers import login, register
from fastapi import FastAPI

app = FastAPI()
app.include_router(register.router)
app.include_router(login.router)