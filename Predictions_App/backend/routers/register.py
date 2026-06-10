#Imports
from fastapi import APIRouter, Depends
from backend.models.models import User
from backend.core.security import hash_password
from backend.core.database import get_db
from sqlalchemy.orm import Session
from backend.schemas.user import UserRegister

#Router
router = APIRouter()

@router.post("/register")

#Define the register function
def register(user: UserRegister, db: Session = Depends(get_db)):
    #Hash password#
    hashed_password = hash_password(user.password)

    #Store user in database
    db.add(User(username=user.username, hashed_password=hashed_password))
    db.commit()
    
    #Return success message
    return {"message": "User registered successfully"}
