from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def me(user = Depends(get_current_user)):
    return user
