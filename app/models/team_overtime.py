# app/models/team_overtime.py

from sqlalchemy import Column, Integer, String
from app.db import Base

class TeamOvertimeStats(Base):
    __tablename__ = "team_overtime_stats"

    team_abbrev = Column(String, primary_key=True)
    games_with_draw = Column(Integer)
    total_games = Column(Integer)
    wins_in_overtime = Column(Integer)
    total_as_underdog = Column(Integer)
    losses_in_overtime = Column(Integer)
    total_as_favorite = Column(Integer)
    wins_ot = Column(Integer)
    losses_ot = Column(Integer)
    wins_so = Column(Integer)
    losses_so = Column(Integer)