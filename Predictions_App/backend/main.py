from fastapi import FastAPI
from backend.routers.auth import register, login
from backend.routers.tournament import GET as tournament_GET, POST as tournament_POST
from backend.routers.predictions import GET as predictions_GET, POST as predictions_POST
from backend.routers.scoreboard import GET as scoreboard_GET
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
