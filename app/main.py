# app/main.py

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.repositories.games import get_games_grouped_by_date_with_cutoff
from app.crud import get_teams_grouped_by_division

from app.repositories.insights_analysis import get_team_upsets_summary
from app.repositories.insights_home_upsets import get_home_upsets_summary
from app.repositories.insights_summary_table import get_summary_table
from app.repositories.insights_stage_upsets import get_stage_upsets_summary
from app.repositories.insights_upset_streaks import get_upset_streaks_summary

from app.routers import game, team, teams

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(game.router)
app.include_router(team.router)
app.include_router(teams.router)


@app.get("/")
async def index(request: Request, page: int = 1, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * 20
    grouped_matches = await get_games_grouped_by_date_with_cutoff(20, offset=offset)
    divisions = await get_teams_grouped_by_division(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "matches_by_date": grouped_matches,
        "divisions": divisions,
        "current_page": page,
    })


@app.get("/insights")
async def insights_page(request: Request, db: AsyncSession = Depends(get_db)):
    upsets_data = await get_team_upsets_summary()
    home_upsets_data = await get_home_upsets_summary()

    top7_upsets = sorted(upsets_data, key=lambda x: x['upset_rate'], reverse=True)[:7]
    top7_home_upsets = sorted(home_upsets_data, key=lambda x: x['home_upset_rate'], reverse=True)[:7]

    summary_table = await get_summary_table()
    stage_upsets = await get_stage_upsets_summary()
    upset_streaks = await get_upset_streaks_summary()

    return templates.TemplateResponse(
        "insights.html",
        {
            "request": request,
            "upsets": top7_upsets,
            "home_upsets": top7_home_upsets,
            "summary_table": summary_table,
            "stage_upsets": stage_upsets,
            "upset_streaks": upset_streaks
        }
    )