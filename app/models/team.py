# app/model/team.py

from app.db import Base
from sqlalchemy import Column, Integer, String, Float

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    abbrev = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    division = Column(String, nullable=False)
    conference = Column(String, nullable=False)

    total_games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)

    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_diff = Column(Integer)
    avg_goals_for = Column(Float(3))
    avg_goals_against = Column(Float(3))

    sog_for = Column(Integer)
    sog_against = Column(Integer)
    avg_sog_for = Column(Float(3))
    avg_sog_against = Column(Float(3))

    avg_faceoff_win_pct = Column(Float(3))

    total_pp_goals = Column(Integer)
    total_pp_attempts = Column(Integer)
    powerplay_pct = Column(Float(3))
    total_pim = Column(Integer)
    avg_pim_per_game = Column(Float(3))

    total_hits = Column(Integer)
    total_blocks = Column(Integer)
    avg_hits = Column(Float(3))
    avg_blocks = Column(Float(3))

    max_win_streak = Column(Integer)
    max_loss_streak = Column(Integer)

    home_wins = Column(Integer)
    home_losses = Column(Integer)
    away_wins = Column(Integer)
    away_losses = Column(Integer)