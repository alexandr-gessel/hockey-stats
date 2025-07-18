# repositories/goalies_repository.py

from sqlalchemy.future import select
from app.models import Goalies
from sqlalchemy.ext.asyncio import AsyncSession


async def get_goalies_by_game_id(db: AsyncSession, game_id: int):
    result = await db.execute(
        select(Goalies)
        .where(Goalies.gameid == game_id)
        .where(Goalies.toi != "00:00")
    )
    goalies = result.scalars().all()

    home_goalies = [g for g in goalies if g.hometeam]
    away_goalies = [g for g in goalies if not g.hometeam]

    return {
        "home": home_goalies,
        "away": away_goalies
    }