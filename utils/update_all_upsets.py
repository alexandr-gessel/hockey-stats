# update_all_upsets.py


import asyncio
from app.db import async_session
from app.models import Team
from app.repositories.upset_updater import update_team_upset
from sqlalchemy import select

async def main():
    async with async_session() as session:
        result = await session.execute(select(Team.abbrev))
        teams = result.scalars().all()

    print(f"Обновляем апсет-метрики для {len(teams)} команд...")

    for team_abbrev in teams:
        print(f" → {team_abbrev}")
        await update_team_upset(team_abbrev)

    print("Готово!")

if __name__ == "__main__":
    asyncio.run(main())