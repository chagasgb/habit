from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database.database import get_db, Base, engine
from models.models import *
from datetime import datetime, date
from typing import List


records_router = APIRouter(prefix="/api", tags=["Habits-records"])

# Rota para adicionar um registro de hábito concluído pelo nome
@records_router.post("/habit/record", response_model=HabitRecordResponse)
def record_habit(record: HabitRecordCreate, db: Session = Depends(get_db)):
    
    habit = db.query(Habit).filter(Habit.name == record.name).first()
    
    new_record = HabitRecord(
        habit_id=habit.id,
        record_datetime=datetime.now()
    )
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record