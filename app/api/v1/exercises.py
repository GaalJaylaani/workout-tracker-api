from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db, get_current_user
from app.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseRead

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("", response_model=ExerciseRead)
def create_exercise(payload: ExerciseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if db.query(Exercise).filter(Exercise.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Exercise already exists")
    ex = Exercise(**payload.dict())
    db.add(ex); db.commit(); db.refresh(ex)
    return ex

@router.get("", response_model=List[ExerciseRead])
def list_exercises(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0), db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Exercise).order_by(Exercise.name).offset(offset).limit(limit).all()

@router.get("/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ex = db.get(Exercise, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="Not found")
    return ex

@router.put("/{exercise_id}", response_model=ExerciseRead)
def update_exercise(exercise_id: int, payload: ExerciseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ex = db.get(Exercise, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in payload.dict().items():
        setattr(ex, k, v)
    db.commit(); db.refresh(ex)
    return ex

@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ex = db.get(Exercise, exercise_id)
    if not ex:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(ex); db.commit()
    return {"ok": True}
