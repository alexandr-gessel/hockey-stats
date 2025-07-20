#app/models/goalsbyperiod.py

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from pydantic import BaseModel
from app.db import Base
from datetime import date

class GoalsByPeriod(Base):
    __tablename__ = "goalsbyperiod"

    id = Column(Integer, primary_key=True, index=True)
    id_game = Column(Integer, nullable=False, index=True)
    p1_home = Column(Integer, nullable=True)
    p1_away = Column(Integer, nullable=True)
    p2_home = Column(Integer, nullable=True)
    p2_away = Column(Integer, nullable=True)
    p3_home = Column(Integer, nullable=True)
    p3_away = Column(Integer, nullable=True)
    p4_home = Column(Integer, nullable=True)
    p4_away = Column(Integer, nullable=True)
    p5_home = Column(Integer, nullable=True)
    p5_away = Column(Integer, nullable=True)
    p6_home = Column(Integer, nullable=True)
    p6_away = Column(Integer, nullable=True)
    p7_home = Column(Integer, nullable=True)
    p7_away = Column(Integer, nullable=True)