# app/repositories/search_players.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import PlayersSummary


async def search_players_by_name(db: AsyncSession, query: str):
    stmt = (
        select(PlayersSummary)
        .where(PlayersSummary.name.ilike(f"%{query}%"))
        .order_by(PlayersSummary.name)
    )
    result = await db.execute(stmt)
    return result.scalars().all()