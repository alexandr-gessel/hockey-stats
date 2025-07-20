# app/models/team_analytics.py

from app.db import Base
from sqlalchemy import Column, Integer, String, Float

class TeamAnalytics(Base):
    __tablename__ = "team_analytics"

    id = Column(Integer, primary_key=True, index=True)
    team_abbrev = Column(String, unique=True, nullable=False, index=True)

    faceoff_win_in_wins = Column(Float(3))
    faceoff_win_in_losses = Column(Float(3))
    pim_in_wins = Column(Float(3))
    pim_in_losses = Column(Float(3))
    shot_goal_corr = Column(Float(3))
    pp_conversion_win_rate = Column(Float(3))

    shot_conversion = Column(Float(3))
    faceoff_win_impact = Column(Float(3))
    hit_to_goal = Column(Float(3))
    block_to_shot = Column(Float(3))