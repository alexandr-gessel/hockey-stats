# app/scripts/save_all_team_overtime_stats.py

import asyncio
from app.db import async_session
from app.models import Team
from app.scripts.save_team_overtime_stats import save_overtime_stats
from sqlalchemy import select

async def update_all_teams():
    async with async_session() as session:
        result = await session.execute(select(Team.abbrev))
        abbrevs = [row[0] for row in result.all()]

    print(f" nicht gefunden {len(abbrevs)}")
    for abbrev in abbrevs:
        print(f" abarbeit {abbrev}...")
        try:
            await save_overtime_stats(abbrev)
        except Exception as e:
            print(f"error {abbrev}: {e}")

if __name__ == "__main__":
    asyncio.run(update_all_teams())