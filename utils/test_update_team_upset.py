# app/test_update_team_upset.py

import asyncio
from app.repositories.upset_updater import update_team_upset

async def main():
    await update_team_upset("MTL")  # BOS

if __name__ == "__main__":
    asyncio.run(main())