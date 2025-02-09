from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from database import SessionLocal
from models import Habit

class HabitCreate(BaseModel):
    name: str
    frequency: int = 1
    active: bool = True
    flexible: bool = False
    
    #verifica se esta vazio
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v

    #verifica se ja existe
    @field_validator('name')
    @classmethod
    def name_must_be_unique(cls, v):
        db = SessionLocal()
        try:
            habit = db.query(Habit).filter(Habit.name == v).first()
            if habit:
                raise ValueError(f"Habit with name '{v}' already exists")
        finally:
            db.close()
        return v


class HabitResponse(BaseModel):
    id: int
    name: str
    frequency: int
    active: bool
    flexible: bool
    records: int
    
    class Config:
        from_attributes = True

#-------------------------------#------------------------ 

class HabitRecordCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def habit_must_exist(cls, v: str) -> str:
        """Valida se o hábito já existe no banco antes de criar um novo registro."""
        db = SessionLocal()
        try:
            habit = db.query(Habit).filter(Habit.name == v).first()
            if not habit:
                raise ValueError(f"Habit '{v}' does not exist")
        finally:
            db.close()
        return v
    
    #verifica se esta vazio
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v

class HabitRecordResponse(BaseModel):
    id: int
    habit_id: int
    record_datetime: Optional[datetime] = None

    class Config:
        from_attributes = True

# Para evitar referências circulares
HabitResponse.model_rebuild()