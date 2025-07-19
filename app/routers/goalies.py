# app/routers/goalies.py

from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session, get_db
from app.models import GoaliesSummary
from app.repositories.search_goalies import search_goalies_by_name

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/goalies", response_class=HTMLResponse)
async def goalies_page(request: Request):
    async with async_session() as session:
        result = await session.execute(
            select(GoaliesSummary).order_by(GoaliesSummary.name)
        )
        goalies = result.scalars().all()
    return templates.TemplateResponse("goalies.html", {
        "request": request,
        "goalies": goalies
    })


@router.get("/goalies/search")
async def search_goalies(
    request: Request,
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    goalies = await search_goalies_by_name(db, q)
    return templates.TemplateResponse(
        "goalies_search.html",
        {"request": request, "goalies": goalies, "query": q}
    )