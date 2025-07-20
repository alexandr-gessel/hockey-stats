# repositories/games.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict
from app.models import Games
from app.db import async_session
from app.crud import get_team_by_abbrev
from app.models import GameShortDTO 

async def get_games(limit: int = 20, offset: int = 0):
    async with async_session() as session:
        result = await session.execute(
            select(Games)
            .order_by(Games.gamedate.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = result.scalars().all()

        games_list = []
        for game in rows:
            home_team_obj = await get_team_by_abbrev(session, game.hometeam)
            away_team_obj = await get_team_by_abbrev(session, game.awayteam)

            dto = GameShortDTO(
				    id_game=game.id_game,
				    date=game.gamedate,
				    home_team=home_team_obj.name if home_team_obj else game.hometeam,
				    home_team_abbr=game.hometeam,
				    away_team=away_team_obj.name if away_team_obj else game.awayteam,
				    away_team_abbr=game.awayteam,
				    score=f"{game.ht_score} – {game.at_score}" if game.ht_score is not None and game.at_score is not None else "–",
				    note=game.period_type or ""
				)
            games_list.append(dto.dict())

        return games_list


async def get_games_grouped_by_date_with_cutoff(limit: int = 20, offset: int = 0, search_team: str = "", search_date: str = ""):
    games = await get_games(limit=500, offset=offset)  # Загружаем с запасом

    filtered = []
    for game in games:
        if search_team:
            if search_team.lower() not in game["home_team"].lower() and search_team.lower() not in game["away_team"].lower():
                continue
        if search_date:
            if game["date"].strftime("%Y-%m-%d") != search_date:
                continue
        filtered.append(game)

    grouped = defaultdict(list)
    for game in filtered:
        grouped[game["date"]].append(game)

    grouped_sorted = sorted(grouped.items(), key=lambda x: x[0], reverse=True)

    result = []
    total_games = 0
    for date, games_list in grouped_sorted:
        result.append((date, games_list))
        total_games += len(games_list)
        if total_games >= limit:
            break

    return result