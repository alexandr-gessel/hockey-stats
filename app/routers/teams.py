# app/routers/teams.py

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud import get_team_by_abbrev
from app.repositories.table_games import get_teams_stats

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/teams")
async def teams_page(request: Request, db: AsyncSession = Depends(get_db)):
    stats_raw = await get_teams_stats(db)
    teams = []

    for row in stats_raw:
        team_obj = await get_team_by_abbrev(db, row["abbr"])
        teams.append({
            "name": team_obj.name if team_obj else row["abbr"],
            "abbr": row["abbr"],
            "games_played": row["games_played"],
            "wins": row["wins"],
            "losses": row["losses"],
            "ties": row["ties"],
            "goals_for": row["goals_for"],
            "goals_against": row["goals_against"],
            "sog_for": row["sog_for"],
            "sog_against": row["sog_against"],
            "faceoff_pct": row["faceoff_pct"],
            "pp_pct": row["pp_pct"],
            "pim": row["pim"],
            "hits": row["hits"],
            "blocks": row["blocks"],
            "goal_diff": row["goal_diff"]
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