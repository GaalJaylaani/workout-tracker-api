from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, Token

ALGO = "HS256"
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = User(email=user.email, password_hash=hash_password(user.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"access_token": create_access_token(str(u.id))}

@router.post("/login", response_model=Token)
def login(creds: UserCreate, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == creds.email).first()
    if not u or not verify_password(creds.password, u.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": create_access_token(str(u.id))}
