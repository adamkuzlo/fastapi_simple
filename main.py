from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User

app = FastAPI()

@app.get("/")
async def root(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Fetch all users with optional pagination.
    - `skip`: Number of records to skip (default: 0).
    - `limit`: Maximum number of records to return (default: 10).
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}

@app.post("/add_user/")
def add_user(name: str, email: str, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user instance
    new_user = User(name=name, email=email)
    
    # Add the new user to the session
    db.add(new_user)
    db.commit()  # Commit the transaction to save to the database
    db.refresh(new_user)  # Refresh to get the updated instance with generated ID
    
    return {"message": "User added successfully", "user_id": new_user.id}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}
