# scripts/test_bio_parser.py

import asyncio
from app.utils.player_bio_parser import get_player_bio

async def main():
    player_id = 8471675  # Sidney Crosby
    bio = await get_player_bio(player_id)
    print(bio)

if __name__ == "__main__":
    asyncio.run(main())