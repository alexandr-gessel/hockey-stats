#

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from app.db import Base
from datetime import date

class Quotes(Base):
    __tablename__ = 'odds'

    id = Column(Integer, primary_key=True)
    name_1 = Column(Text, nullable=False)
    name_2 = Column(Text, nullable=False)
    quote_1 = Column(Float, nullable=False)
    quote_un = Column(Float, nullable=True)
    quote_2 = Column(Float, nullable=False)
    spieldate = Column(Date, nullable=False)
    win = Column(Float, nullable=True)
    play_off = Column(Boolean, nullable=False)
    unentschieden = Column(Boolean, nullable=False)
    note = Column(Text, nullable=True)
    pre_season = Column(Boolean, nullable=False)