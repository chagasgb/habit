from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Habit, HabitRecord
from schemas import HabitCreate, HabitResponse, HabitRecordCreate, HabitRecordResponse
from sqlalchemy import func

habits_router = APIRouter(prefix="/habits", tags=["Habits"])

"""
NOVO HABITO
"""
@habits_router.post("/add", response_model=HabitResponse)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    new_habit = Habit(
        name=habit.name,
        frequency=habit.frequency,
        active=habit.active,
        flexible=habit.flexible
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    
    record_count = len(new_habit.records)
    habit_response = HabitResponse(
        id=new_habit.id,
        name=new_habit.name,
        frequency=new_habit.frequency,
        active=new_habit.active,
        flexible=new_habit.flexible,
        records=record_count
    )
    
    return habit_response

"""
DELETE HABITO
"""
@habits_router.delete("/delete/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    
    ############### EPAAAAAAAAA
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
            Habit.frequency,
            Habit.active,
            Habit.flexible,
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
            frequency=result.frequency,
            active=result.active,
            flexible=result.flexible,
            records=result.records
        )
        for result in results
    ]
    return habit_responses
    