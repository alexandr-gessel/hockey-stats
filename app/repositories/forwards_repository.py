# repositories/forwards_repository.py

from sqlalchemy.future import select
from app.models import ForwardsDefense
from sqlalchemy.ext.asyncio import AsyncSession


async def get_forwards_by_game_id(db: AsyncSession, game_id: int):
    result = await db.execute(
        select(ForwardsDefense).where(ForwardsDefense.gameid == game_id)
    )
    players = result.scalars().all()

    # Добавляем свойство toi_seconds к каждому игроку
    for p in players:
        p.toi_seconds = parse_toi_to_seconds(p.toi)
    return players


def parse_toi_to_seconds(toi: str | None) -> int:
    if not toi or ":" not in toi:
        return 0
    try:
        minutes, seconds = map(int, toi.split(":"))
        return minutes * 60 + seconds
    except Exception:
        return 0

def select_top_players_by_team(players, is_home):
    team_players = [p for p in players if p.hometeam == is_home]

    def get_max(players, attr):
        return max(players, key=lambda p: getattr(p, attr) or 0) if players else None

    return {
        "most_points": get_max(team_players, "points"),
        "most_toi": get_max(team_players, "toi_seconds"),
        "most_hits": get_max(team_players, "hits"),
        "best_plusminus": get_max(team_players, "plusminus"),
        "most_shots": get_max(team_players, "shots"),
    }