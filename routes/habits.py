from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import *
from sqlalchemy import func
from services.habit_service import check_habit_exists

habits_router = APIRouter(prefix="/habits", tags=["Habits"])

"""
NOVO HABITO
"""
@habits_router.post("/add")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    
    check_habit_exists(db, habit.name)
    
    #criação
    new_habit = Habit(
        name=habit.name,
        dias_da_semana=habit.dias_da_semana,
        active=habit.active,
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    
    return new_habit

"""
DELETE HABITO
"""
@habits_router.delete("/delete/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    
    if not habit:
        raise HTTPException(status_code=404, detail="Hábito não encontrado")
    
    db.delete(habit)
    db.commit()
    return {"message": f"Hábito {habit_id} deletado com sucesso!"}


"""
GET HABITOS
"""
@habits_router.get("", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    results = (
        db.query(
            Habit.id,
            Habit.name,
            Habit.dias_da_semana,
            Habit.active,
            func.count(HabitRecord.id).label('records')
        )
        .outerjoin(HabitRecord)
        .group_by(Habit.id)
        .all()
    )
    habit_responses = [
        HabitResponse(
            id=result.id,
            name=result.name,
            dias_da_semana=result.dias_da_semana,
            active=result.active,
            records=result.records
        )
        for result in results
    ]
    return habit_responses
    