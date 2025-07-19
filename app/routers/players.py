# app/routers/players.py

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session, get_db
from app.models import PlayersSummary

from app.repositories.search_players import search_players_by_name


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/players", response_class=HTMLResponse)
async def teams_page(request: Request):
    async with async_session() as session:
        result = await session.execute(
            select(PlayersSummary).order_by(PlayersSummary.name)
        )
        players = result.scalars().all()
    return templates.TemplateResponse("players.html", {
        "request": request,
        "players": players
    })

@router.get("/players/search")
async def search_players(
    request: Request,
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    players = await search_players_by_name(db, q)
    return templates.TemplateResponse(
        "players_search.html",
        {"request": request, "players": players, "query": q}
    )