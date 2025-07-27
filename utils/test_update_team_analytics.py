# test_update_team_analytics.py

import asyncio
from app.repositories.team_analytics_updater import update_team_analytics

async def main():
    await update_team_analytics("VAN") 
if __name__ == "__main__":
    asyncio.run(main())