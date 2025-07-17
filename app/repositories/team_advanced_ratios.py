# repositories/team_advanced_ratios.py

from app.db import async_session
from app.crud import get_team_by_abbrev
from sqlalchemy import select, or_
from app.models import Games

async def get_advanced_ratios(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            return {}

        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.scalars().all()

        if not games:
            return {}

        total_goals = 0
        total_shots = 0
        total_hits = 0
        total_blocks = 0
        total_opponent_shots = 0

        faceoff_win_games = 0
        total_games = 0

        for game in games:
            if game.hometeam == team_abbrev:
                goals = game.ht_score
                shots = game.ht_sog
                faceoff = game.ht_faceoffwinningpctg
                hits = game.ht_hits
                blocks = game.ht_blocks
                opponent_shots = game.at_sog
                won = game.ht_score > game.at_score
            else:
                goals = game.at_score
                shots = game.at_sog
                faceoff = game.at_faceoffwinningpctg
                hits = game.at_hits
                blocks = game.at_blocks
                opponent_shots = game.ht_sog
                won = game.at_score > game.ht_score

            total_games += 1

            if shots is not None:
                total_shots += shots
            if goals is not None:
                total_goals += goals
            if hits is not None:
                total_hits += hits
            if blocks is not None:
                total_blocks += blocks
            if opponent_shots is not None:
                total_opponent_shots += opponent_shots

            if faceoff is not None and faceoff > 50 and won:
                faceoff_win_games += 1

        def safe_div(a, b):
            return round(a / b, 2) if b else 0

        return {
            "shot_conversion": safe_div(total_goals, total_shots) * 100,  # в процентах
            "faceoff_win_impact": round(safe_div(faceoff_win_games, total_games) * 100, 2),
            "hit_to_goal": safe_div(total_hits, total_goals),
            "block_to_shot": safe_div(total_blocks, total_opponent_shots) * 100  # в процентах
        }