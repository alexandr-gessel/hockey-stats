# app/routers/game.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.crud import get_game_by_id, get_team_by_abbrev, get_goals_by_game_id
from app.repositories.team_form import get_team_last_games, calculate_avg_goal_diff, get_streak, get_game_result
from app.repositories.goalies_repository import get_goalies_by_game_id
from app.repositories.forwards_repository import get_forwards_by_game_id, select_top_players_by_team
from app.utils.team_colors import get_team_color

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def build_period_scores(goals_by_period):
    periods = []
    for i in range(1, 8):
        home = getattr(goals_by_period, f"p{i}_home", None)
        away = getattr(goals_by_period, f"p{i}_away", None)
        if home is not None or away is not None:
            periods.append({
                "period": i,
                "home": home,
                "away": away
            })
    return periods


@router.get("/game/{game_id}")
async def read_game(game_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    match = await get_game_by_id(db, game_id)
    if not match:
        raise HTTPException(status_code=404, detail="Game not found")

    home_team = await get_team_by_abbrev(db, match.hometeam)
    away_team = await get_team_by_abbrev(db, match.awayteam)

    if not home_team or not away_team:
        raise HTTPException(status_code=404, detail="Team not found")

    home_games = await get_team_last_games(match.hometeam)
    away_games = await get_team_last_games(match.awayteam)

    home_form = {
        "results": [get_game_result(g, match.hometeam) for g in home_games],
        "avg_diff": calculate_avg_goal_diff(home_games, match.hometeam),
        "streak": get_streak(home_games, match.hometeam)
    }

    away_form = {
        "results": [get_game_result(g, match.awayteam) for g in away_games],
        "avg_diff": calculate_avg_goal_diff(away_games, match.awayteam),
        "streak": get_streak(away_games, match.awayteam)
    }

    goals_by_period = await get_goals_by_game_id(db, match.id_game)
    period_scores = build_period_scores(goals_by_period) if goals_by_period else []

    goalies = await get_goalies_by_game_id(db, match.id_game)
    forwards = await get_forwards_by_game_id(db, match.id_game)

    home_top_players = select_top_players_by_team(forwards, is_home=True)
    away_top_players = select_top_players_by_team(forwards, is_home=False)

    return templates.TemplateResponse("game.html", {
        "request": request,
        "match": match,
        "home_team": home_team,
        "away_team": away_team,
        "home_form": home_form,
        "away_form": away_form,
        "home_color": get_team_color(match.hometeam),
        "away_color": get_team_color(match.awayteam),
        "period_scores": period_scores,
        "goalies": goalies,
        "top_players_home": home_top_players,
        "top_players_away": away_top_players,
    })