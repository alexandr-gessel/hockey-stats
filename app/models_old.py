#app/models.py

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from pydantic import BaseModel
from app.db import Base
from datetime import date



class ForwardsDefense(Base):
    __tablename__ = "forwards_defense"

    id = Column(Integer, primary_key=True, index=True)
    gameid = Column(Integer, index=True, nullable=False)
    hometeam = Column(Boolean, nullable=False)
    playerid = Column(Integer, nullable=False)
    sweaternumber = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    goals = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    points = Column(Integer, nullable=True)
    plusminus = Column(Integer, nullable=True)
    pim = Column(Integer, nullable=True)
    hits = Column(Integer, nullable=True)
    blockedshots = Column(Integer, nullable=True)
    powerplaygoals = Column(Integer, nullable=True)
    powerplaypoints = Column(Integer, nullable=True)
    shorthandedgoals = Column(Integer, nullable=True)
    shpoints = Column(Integer, nullable=True)
    shots = Column(Integer, nullable=True)
    faceoffs = Column(String, nullable=True)  # дробь вида "8/14"
    faceoffwinningpctg = Column(Float, nullable=True)
    toi = Column(String, nullable=True)  # "05:35"
    powerplaytoi = Column(String, nullable=True)
    shorthandedtoi = Column(String, nullable=True)


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




