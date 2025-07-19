#app/models.py

from sqlalchemy import Column, Integer, String, Date, Float, Boolean, Text
from pydantic import BaseModel
from app.db import Base
from datetime import date

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    abbrev = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    division = Column(String, nullable=False)
    conference = Column(String, nullable=False)

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


class GameShortDTO(BaseModel):
    id_game: int
    date: date
    home_team: str
    home_team_abbr: str
    away_team: str
    away_team_abbr: str
    score: str
    note: str


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

class GoalsByPeriod(Base):
    __tablename__ = "goalsbyperiod"

    id = Column(Integer, primary_key=True, index=True)
    id_game = Column(Integer, nullable=False, index=True)
    p1_home = Column(Integer, nullable=True)
    p1_away = Column(Integer, nullable=True)
    p2_home = Column(Integer, nullable=True)
    p2_away = Column(Integer, nullable=True)
    p3_home = Column(Integer, nullable=True)
    p3_away = Column(Integer, nullable=True)
    p4_home = Column(Integer, nullable=True)
    p4_away = Column(Integer, nullable=True)
    p5_home = Column(Integer, nullable=True)
    p5_away = Column(Integer, nullable=True)
    p6_home = Column(Integer, nullable=True)
    p6_away = Column(Integer, nullable=True)
    p7_home = Column(Integer, nullable=True)
    p7_away = Column(Integer, nullable=True)

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
