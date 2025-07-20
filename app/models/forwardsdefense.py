#app/models/forwardsdefense.py

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
