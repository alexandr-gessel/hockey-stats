# app/models/upset.py

from sqlalchemy import Column, Integer, String, Float
from app.db import Base

class Upset(Base):
    __tablename__ = "upset"

    id = Column(Integer, primary_key=True, index=True)
    team_abbrev = Column(String, unique=True, nullable=False, index=True)

    total_games = Column(Integer)
    num_upsets = Column(Integer)
    upset_share = Column(Float(3))
    avg_upset_quote = Column(Float(3))

    regular_total = Column(Integer)
    regular_upsets = Column(Integer)
    preseason_total = Column(Integer)
    preseason_upsets = Column(Integer)
    playoff_total = Column(Integer)
    playoff_upsets = Column(Integer)

    total_games_with_high_quote = Column(Integer)
    upsets_with_high_quote = Column(Integer)
    share_with_high_quote = Column(Float(3))

    total_home_games = Column(Integer)
    home_fav_losses = Column(Integer)
    home_loss_share = Column(Float(3))

    real_win_rate = Column(Float(3))
    expected_win_rate = Column(Float(3))
    max_upset_streak = Column(Integer)
    max_fav_loss_streak = Column(Integer)