# update_all_team_analytics.py

import asyncio
from app.db import async_session
from app.models import Team
from app.repositories.team_analytics_updater import update_team_analytics
from sqlalchemy import select

async def main():
    async with async_session() as session:
        result = await session.execute(select(Team.abbrev))
        teams = result.scalars().all()

    print(f"Обновляем аналитические метрики для {len(teams)} команд...")

    for team_abbrev in teams:
        print(f" → {team_abbrev}")
        await update_team_analytics(team_abbrev)

    print("Готово!")

if __name__ == "__main__":
    asyncio.run(main())
