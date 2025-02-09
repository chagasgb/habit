from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base
from datetime import date, datetime

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)  # Adicionado unique=True para garantir nomes únicos
    frequency = Column(Integer, default=1)
    active = Column(Boolean, default=True)
    flexible = Column(Boolean, default=False)
    records = relationship("HabitRecord", back_populates="habit")

class HabitRecord(Base):
    __tablename__ = "habit_records"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date, default=date.today)
    record_datetime = Column(DateTime, default=datetime.now)  # Usar DateTime do SQLAlchemy
    habit = relationship("Habit", back_populates="records")
