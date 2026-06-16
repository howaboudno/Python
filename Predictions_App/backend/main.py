from routers.auth import register, login
from routers.tournament import GET as tournament_GET, POST as tournament_POST
from routers.predictions import GET as predictions_GET, POST as predictions_POST
from routers.scoreboard import GET as scoreboard_GET
from routers.auth import change_password
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "null",
        "https://python-production-c646.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(login.router)
app.include_router(tournament_GET.router)
app.include_router(tournament_POST.router)
app.include_router(predictions_GET.router)
app.include_router(predictions_POST.router)
app.include_router(scoreboard_GET.router)
app.include_router(change_password.router)
