from routers.auth import register, login
from routers.tournament import GET as tournament_GET, POST as tournament_POST
from routers.predictions import GET as predictions_GET, POST as predictions_POST
from routers.scoreboard import GET as scoreboard_GET
from routers.auth import change_password
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import shutil
from fastapi import UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "null",
        "https://python-production-c646.up.railway.app",
        "https://predictionsapp.vercel.app"
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

@app.post("/admin/upload-db")
async def upload_db(file: UploadFile = File(...)):
    with open("/data/predictions.db", "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"message": "Database uploaded"}

@app.get("/admin/download-db")
def download_db():
    return FileResponse("/data/predictions.db", filename="predictions.db")

@app.post("/admin/dedupe-predictions")
def dedupe_predictions():
    from core.database import SessionLocal
    from sqlalchemy import text
    db = SessionLocal()
    try:
        db.execute(text("""
            DELETE FROM fixture_predictions
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM fixture_predictions
                GROUP BY user_id, fixture_id
            )
        """))
        db.commit()
        return {"message": "Deduped"}
    finally:
        db.close()
        
@app.post("/admin/dedupe-results")
def dedupe_predictions():
    from core.database import SessionLocal
    from sqlalchemy import text
    db = SessionLocal()
    try:
        db.execute(text("""
            DELETE FROM results
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM results
                GROUP BY fixture_id
            )
        """))
        db.commit()
        return {"message": "Deduped"}
    finally:
        db.close()