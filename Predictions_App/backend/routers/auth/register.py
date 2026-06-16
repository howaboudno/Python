#Imports
from fastapi import APIRouter, Depends, HTTPException, status
from models.models import User
from core.security import hash_password
from core.database import get_db
from sqlalchemy.orm import Session
from schemas.user import UserRegister

#Router
router = APIRouter()

@router.post("/register")

#Define the register function
def register(user: UserRegister, db: Session = Depends(get_db)):
    #Check if user already exists
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User already exists, contact admin for details or in  case of forgotton password")

    hashed_password = hash_password(user.password)

    #Store user in database
    db.add(User(
            username=user.username,
            hashed_password=hashed_password))
    db.commit()

    #Return success message
    return {"message": "User registered successfully"}
