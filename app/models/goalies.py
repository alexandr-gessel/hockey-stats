# app/models/goalies.py

from app.db import Base
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text

class Goalies(Base):
    __tablename__ = "goalies"

    id = Column(Integer, primary_key=True, index=True)
    gameid = Column(Integer, index=True, nullable=False)
    hometeam = Column(Boolean, nullable=False)
    playerid = Column(Integer, nullable=False)
    sweaternumber = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    evenstrengthshotsagainst = Column(String, nullable=True)  # как "8/10"
    powerplayshotsagainst = Column(String, nullable=True)
    shorthandedshotsagainst = Column(String, nullable=True)
    saveshotsagainst = Column(String, nullable=True)
    savepctg = Column(Float, nullable=True)
    evenstrengthgoalsagainst = Column(Integer, nullable=True)
    powerplaygoalsagainst = Column(Integer, nullable=True)
    shorthandedgoalsagainst = Column(Integer, nullable=True)
    pim = Column(Integer, nullable=True)
    goalsagainst = Column(Integer, nullable=True)
    toi = Column(String, nullable=True)  # "58:23"


class GoaliesSummary(Base):
    __tablename__ = "goalies_summary"

    id = Column(Integer, primary_key=True, index=True)
    playerid = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    games_played = Column(Integer, default=0)
    
    evenstrengthshotsagainst = Column(Integer, default=0)
    powerplayshotsagainst = Column(Integer, default=0)
    shorthandedshotsagainst = Column(Integer, default=0)
    saveshotsagainst = Column(Integer, default=0)
    savepctg = Column(Float, default=0.0)
    
    evenstrengthgoalsagainst = Column(Integer, default=0)
    powerplaygoalsagainst = Column(Integer, default=0)
    shorthandedgoalsagainst = Column(Integer, default=0)
    
    goalsagainst = Column(Integer, default=0)
    pim = Column(Integer, default=0)
    toi_total = Column(Integer, default=0)  # в секундах!
