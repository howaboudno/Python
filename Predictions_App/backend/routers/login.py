#Imports
from fastapi import APIRouter, Depends
from backend.models.models import User
from backend.core.security import verify_password, create_access_token
from backend.core.database import get_db
from sqlalchemy.orm import Session
from backend.schemas.user import UserLogin

#Router
router = APIRouter()

@router.post("/login") 
#Define the login function
def login(user: UserLogin, db: Session = Depends(get_db)):
    #Check if user exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        return {"message": "Invalid username"}
    #Verify password
    if not verify_password(user.password, db_user.hashed_password):
        return {"message": "Invalid password"}
    
    #Return success message and generate token
    access_token = create_access_token(user_id=str(db_user.id))
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
