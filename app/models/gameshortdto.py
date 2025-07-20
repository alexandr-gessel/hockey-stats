#app/models/gameshortdto.py

from pydantic import BaseModel
from datetime import date




class GameShortDTO(BaseModel):
    id_game: int
    date: date
    home_team: str
    home_team_abbr: str
    away_team: str
    away_team_abbr: str
    score: str
    note: str