#repositories/team_form.py

from sqlalchemy.future import select
from sqlalchemy import or_
from app.models import Games
from app.db import async_session


async def get_team_last_games(team_abbrev: str, limit: int = 5):
    async with async_session() as session:
        result = await session.execute(
            select(Games)
            .where(or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev))
            .order_by(Games.gamedate.desc())
            .limit(limit)
        )
        return result.scalars().all()


def calculate_avg_goal_diff(games: list, team_abbrev: str):
    if not games:
        return 0
    total_diff = 0
    for game in games:
        if game.hometeam == team_abbrev:
            diff = (game.ht_score or 0) - (game.at_score or 0)
        else:
            diff = (game.at_score or 0) - (game.ht_score or 0)
        total_diff += diff
    return round(total_diff / len(games), 2)


def get_game_result(game, team_abbrev: str):
    if game.hometeam == team_abbrev:
        goals_for = game.ht_score or 0
        goals_against = game.at_score or 0
    else:
        goals_for = game.at_score or 0
        goals_against = game.ht_score or 0

    if goals_for > goals_against:
        return "W"
    elif goals_for < goals_against:
        if game.period_type in ["OT", "SO"]:
            return "OTL"
        return "L"
    else:
        return "T"


def get_streak(games: list, team_abbrev: str):
    if not games:
        return "-"
    last_result = get_game_result(games[0], team_abbrev)
    count = 0
    for game in games:
        if get_game_result(game, team_abbrev) == last_result:
            count += 1
        else:
            break
    return f"{last_result}{count}"