
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from app.db import Base

class Games(Base):
    __tablename__ = 'gamecenter'

    id = Column(Integer, primary_key=True)
    gamedate = Column(Date, nullable=False)
    starttimeutc = Column(Date, nullable=True)
    period_number = Column(Integer, nullable=True)
    hometeam = Column(Text, nullable=False)
    ht_score = Column(Integer, nullable=True)
    ht_sog = Column(Integer, nullable=True)
    ht_faceoffwinningpctg = Column(Integer, nullable=True)
    ht_powerplayconversion = Column(String, nullable=True)
    ht_pim = Column(Integer, nullable=True)
    ht_hits = Column(Integer, nullable=True)
    ht_blocks = Column(Integer, nullable=True)
    awayteam = Column(Text, nullable=False)
    at_score = Column(Integer, nullable=True)
    at_sog = Column(Integer, nullable=True)
    at_faceoffwinningpctg = Column(Integer, nullable=True)
    at_powerplayconversion = Column(String, nullable=True)
    at_pim = Column(Integer, nullable=True)
    at_hits = Column(Integer, nullable=True)
    at_blocks = Column(Integer, nullable=True)
    period_type = Column(Text, nullable=True)
    gametype = Column(Integer, nullable=True)
    json_link = Column(Text, nullable=True)
    id_game = Column(Integer, nullable=True)