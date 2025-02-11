from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import Habit


def check_habit_exists(db: Session, name: str):
    existing_habit = db.query(Habit).filter(Habit.name == name).first()
    if existing_habit:
        raise HTTPException(status_code=400, detail=f"Habito com o nome '{name}' já existe no banco de dados")