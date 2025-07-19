# app/routers/player.py

from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_db
from app.models import PlayersSummary
from app.utils.player_bio_parser import get_player_bio
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/player/{player_id}", response_class=HTMLResponse)
async def player_page(player_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlayersSummary).where(PlayersSummary.playerid == player_id)
    )
    player = result.scalar_one_or_none()

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    bio = await get_player_bio(player_id)

    return templates.TemplateResponse("player.html", {
        "request": request,
        "player": player,
        "bio": bio
    })