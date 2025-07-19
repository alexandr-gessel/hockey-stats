# app/routers/goalie.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models import GoaliesSummary
from app.utils.player_bio_parser import get_player_bio

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/goalie/{player_id}", response_class=HTMLResponse)
async def goalie_page(request: Request, player_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(GoaliesSummary).where(GoaliesSummary.playerid == player_id)
    )
    goalie = result.scalars().first()

    if not goalie:
        raise HTTPException(status_code=404, detail="Goalie not found")

    bio = await get_player_bio(player_id)

    return templates.TemplateResponse("goalie.html", {
        "request": request,
        "goalie": goalie,
        "bio": bio
    })