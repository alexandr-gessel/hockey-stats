# app/routers/teams.py

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud import get_team_by_abbrev, get_all_teams_stats

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/teams")
async def teams_page(request: Request, db: AsyncSession = Depends(get_db)):
    
    team_objects = await get_all_teams_stats(db)

    teams = []

    for team in team_objects:
        teams.append({
            "name": team.name,
            "abbr": team.abbrev,
            "games_played": team.total_games,
            "wins": team.wins,
            "losses": team.losses,
            "ties": team.draws,
            "goals_for": team.goals_for,
            "goals_against": team.goals_against,
            "sog_for": team.sog_for,
            "sog_against": team.sog_against,
            "faceoff_pct": team.avg_faceoff_win_pct,
            "pp_pct": team.powerplay_pct,
            "pim": team.total_pim,
            "hits": team.total_hits,
            "blocks": team.total_blocks,
            "goal_diff": team.goal_diff
        })

    top_wins = sorted(teams, key=lambda t: t["wins"], reverse=True)[:3]
    top_goal_diff = sorted(teams, key=lambda t: t["goal_diff"], reverse=True)[:3]
    top_faceoff = sorted(teams, key=lambda t: t["faceoff_pct"], reverse=True)[:3]
    top_powerplay = sorted(teams, key=lambda t: t["pp_pct"], reverse=True)[:3]
    top_hits = sorted(teams, key=lambda t: t["hits"], reverse=True)[:3]

    return templates.TemplateResponse(
        "teams.html",
        {
            "request": request,
            "teams": teams,
            "top_wins": top_wins,
            "top_goal_diff": top_goal_diff,
            "top_faceoff": top_faceoff,
            "top_powerplay": top_powerplay,
            "top_hits": top_hits,
        }
    )