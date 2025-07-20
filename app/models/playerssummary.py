#app/models/playerssummary.py

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from pydantic import BaseModel
from app.db import Base
from datetime import date


class PlayersSummary(Base):
    __tablename__ = "players_summary"

    id = Column(Integer, primary_key=True, index=True)
    playerid = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    games_played = Column(Integer, default=0)
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    points = Column(Integer, default=0)
    plusminus = Column(Integer, default=0)
    hits = Column(Integer, default=0)
    blockedshots = Column(Integer, default=0)
    pim = Column(Integer, default=0)
    shots = Column(Integer, default=0)
    faceoffs = Column(Integer, default=0)
    faceoffwinningpctg = Column(Float, default=0.0)
    toi_total = Column(Integer, default=0)  # в секундах!
