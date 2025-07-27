# scripts/export_games_to_json.py

import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import async_session
from app.models import Games, Team, GameShortDTO
from sqlalchemy import select

async def main():
    async with async_session() as session:
        # all games
        games_result = await session.execute(
            select(Games).order_by(Games.gamedate.desc())
        )
        games = games_result.scalars().all()

        # abbrev -> name
        teams_result = await session.execute(select(Team.abbrev, Team.name))
        team_map = {abbrev: name for abbrev, name in teams_result.all()}

        # list DTO
        dto_list = []
        for game in games:
            dto = GameShortDTO(
                id_game=game.id_game,
                date=game.gamedate,
                home_team=team_map.get(game.hometeam, game.hometeam),
                home_team_abbr=game.hometeam,
                away_team=team_map.get(game.awayteam, game.awayteam),
                away_team_abbr=game.awayteam,
                score=f"{game.ht_score} – {game.at_score}" if game.ht_score is not None and game.at_score is not None else "–",
                note=game.period_type or ""
            )
            dto_list.append(dto.dict())

        # JSON
        with open("app/static/data/games.json", "w") as f:
            json.dump(dto_list, f, indent=2, default=str)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())