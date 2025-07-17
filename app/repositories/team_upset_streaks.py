# repositories/team_upset_streaks.py

from sqlalchemy import select, or_, and_
from datetime import timedelta
from collections import defaultdict
from app.db import async_session
from app.models import Games, Quotes
from app.crud import get_team_by_abbrev
from app.utils.upset_rules import is_upset_relative

async def get_max_upset_streak(team_abbrev: str, percent_diff: float = 0.25):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return 0

        team_full_name = team.name

        result = await session.execute(
            select(Games, Quotes).join(
                Quotes,
                and_(
                    Quotes.spieldate.between(Games.gamedate - timedelta(days=1), Games.gamedate + timedelta(days=1)),
                    or_(Quotes.name_1 == team_full_name, Quotes.name_2 == team_full_name)
                )
            ).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            ).order_by(Games.gamedate)
        )

        rows = result.fetchall()

        max_streak = 0
        current_streak = 0

        for game, quote in rows:
            if game.hometeam == team_abbrev:
                opponent_abbrev = game.awayteam
            else:
                opponent_abbrev = game.hometeam

            opponent = await get_team_by_abbrev(session, opponent_abbrev)
            if not opponent:
                continue

            if not (
                (quote.name_1 == team_full_name and quote.name_2 == opponent.name) or
                (quote.name_2 == team_full_name and quote.name_1 == opponent.name)
            ):
                continue

            if quote.name_1 == team_full_name:
                team_quote = quote.quote_1
                opponent_quote = quote.quote_2
            else:
                team_quote = quote.quote_2
                opponent_quote = quote.quote_1

            is_winner = (
                (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                (game.awayteam == team_abbrev and game.at_score > game.ht_score)
            )

            if is_upset_relative(team_quote, opponent_quote, percent_diff) and is_winner:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

async def get_max_fav_loss_streak(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
        	print(f"Team {team_abbrev} nicht gefunden.")
        	return 0

        team_full_name = team.name

        result = await session.execute(
            select(Games, Quotes).join(
                Quotes,
                and_(
                    Quotes.spieldate.between(Games.gamedate - timedelta(days=1), Games.gamedate + timedelta(days=1)),
                    or_(Quotes.name_1 == team_full_name, Quotes.name_2 == team_full_name)
                )
            ).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            ).order_by(Games.gamedate)
        )

        rows = result.fetchall()

        max_streak = 0
        current_streak = 0

        for game, quote in rows:
            if game.hometeam == team_abbrev:
                opponent_abbrev = game.awayteam
            else:
                opponent_abbrev = game.hometeam

            opponent = await get_team_by_abbrev(session, opponent_abbrev)
            if not opponent:
                continue

            if not (
                (quote.name_1 == team_full_name and quote.name_2 == opponent.name) or
                (quote.name_2 == team_full_name and quote.name_1 == opponent.name)
            ):
                continue

            if quote.name_1 == team_full_name:
                team_quote = quote.quote_1
                opponent_quote = quote.quote_2
            else:
                team_quote = quote.quote_2
                opponent_quote = quote.quote_1

            is_lost = (
                (game.hometeam == team_abbrev and game.ht_score < game.at_score) or
                (game.awayteam == team_abbrev and game.at_score < game.ht_score)
            )

            if team_quote < opponent_quote and is_lost:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak