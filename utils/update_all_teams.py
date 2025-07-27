#update_all_teams.py

import asyncio
from app.db import async_session
from app.models import Team
from app.repositories.team_stats_updater import update_team_stats
from sqlalchemy import select

async def main():
    async with async_session() as session:
        result = await session.execute(select(Team.abbrev))
        teams = result.scalars().all()

    print(f"Обновляем статистику для {len(teams)} команд...")

    for team_abbrev in teams:
        print(f" → {team_abbrev}")
        await update_team_stats(team_abbrev)

    print("Готово!")

if __name__ == "__main__":
    asyncio.run(main())