from sqlalchemy import JSON, Column, Integer, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import date, datetime
from database.database import Base, SessionLocal
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    dias_da_semana = Column(JSON, nullable=False)
    active = Column(Boolean, default=True)
    records = relationship("HabitRecord", back_populates="habit")
    
    class Config:
        from_attributes = True
        
class MetaSemanal(Habit):
    objetivo: int
    
    def atualizar_progresso(self, quantidade: int):
        self.progresso += quantidade
        self.concluido = self.progresso >= self.objetivo
        return 

#modelos pydantic        
class HabitCreate(BaseModel):
    name: str
    dias_da_semana: list
    active: bool = True

class HabitResponse(BaseModel):
    id: int
    name: str
    dias_da_semana: list
    active: bool
    records: int
    
    class Config:
        from_attributes = True
        
#----------------------------------#

class HabitRecord(Base):
    __tablename__ = "habit_records"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, default=date.today)
    record_datetime = Column(DateTime, default=datetime.now)
    habit = relationship("Habit", back_populates="records")
    
    class Config:
        from_attributes = True

#modelos pydantic
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