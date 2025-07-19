# repositories/search_goalies.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import GoaliesSummary

async def search_goalies_by_name(db: AsyncSession, query: str):
    result = await db.execute(
        select(GoaliesSummary)
        .where(GoaliesSummary.name.ilike(f"%{query}%"))
        .order_by(GoaliesSummary.name)
    )
    return result.scalars().all()