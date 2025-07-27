# test_update_team.py

import asyncio
from app.repositories.team_stats_updater import update_team_stats

async def main():
    await update_team_stats("CGY") 

if __name__ == "__main__":
    asyncio.run(main())