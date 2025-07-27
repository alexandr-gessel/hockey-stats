#run_get_upsets.py

import asyncio
from app.repositories.team_upset_repository import get_team_upsets

async def main():
    upsets = await get_team_upsets("BOS", threshold_diff=0.2)
    print(f"Найдено апсетов: {len(upsets)}")
    for game, quote in upsets:
        print(f"{game.gamedate} — {game.hometeam} {game.ht_score}:{game.at_score} {game.awayteam}")
        print(f"Коэффициенты: {quote.name_1} — {quote.quote_1} | {quote.name_2} — {quote.quote_2}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())