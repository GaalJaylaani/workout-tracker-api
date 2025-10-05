from pydantic import BaseModel
from typing import Optional

class ExerciseCreate(BaseModel):
    name: str
    muscle_group: str
    equipment: Optional[str] = None

class ExerciseRead(BaseModel):
    id: int
    name: str
    muscle_group: str
    equipment: Optional[str] = None
    class Config:
        from_attributes = True
