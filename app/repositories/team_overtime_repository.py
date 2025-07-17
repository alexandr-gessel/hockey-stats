# repositories/team_overtime_repository.py

from app.utils.upset_rules import is_upset_relative
from app.db import async_session
from app.crud import get_team_by_abbrev
from sqlalchemy import select, or_, and_
from app.models import Games, Quotes
from datetime import timedelta

async def get_draws_in_regular_time(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return {"total_games": 0,"games_with_draw": 0}

        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_games = 0
        games_with_draw = 0

        for game, in games:
            total_games += 1
            if game.period_number > 3:
                games_with_draw += 1

        return {"total_games": total_games, "games_with_draw": games_with_draw}

async def get_upset_wins_in_overtime(team_abbrev: str, percent_diff: float = 0.25):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return { "total_as_underdog": 0, "wins_in_overtime": 0 }

        team_full_name = team.name

        result = await session.execute(
            select(Games, Quotes).join(
                Quotes,
                and_(
                    Quotes.spieldate.between(Games.gamedate - timedelta(days=1), Games.gamedate + timedelta(days=1)),
                    or_(
                        Quotes.name_1 == team_full_name,
                        Quotes.name_2 == team_full_name
                    )
                )
            ).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )

        rows = result.fetchall()

        total_as_underdog = 0
        wins_in_overtime = 0

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

            if is_upset_relative(team_quote, opponent_quote, percent_diff):
                total_as_underdog += 1
                is_winner = (
                    (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                    (game.awayteam == team_abbrev and game.at_score > game.ht_score)
                )
                if is_winner and game.period_type in ("OT", "SO"):
                    wins_in_overtime += 1

        return { "total_as_underdog": total_as_underdog, "wins_in_overtime": wins_in_overtime }

async def get_favorite_losses_in_overtime(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return {
                "total_as_favorite": 0,
                "losses_in_overtime": 0
            }

        team_full_name = team.name

        result = await session.execute(
            select(Games, Quotes).join(
                Quotes,
                and_(
                    Quotes.spieldate.between(Games.gamedate - timedelta(days=1), Games.gamedate + timedelta(days=1)),
                    or_(
                        Quotes.name_1 == team_full_name,
                        Quotes.name_2 == team_full_name
                    )
                )
            ).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )

        rows = result.fetchall()

        total_as_favorite = 0
        losses_in_overtime = 0

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

            if team_quote < opponent_quote:
                total_as_favorite += 1
                is_lost = (
                    (game.hometeam == team_abbrev and game.ht_score < game.at_score) or
                    (game.awayteam == team_abbrev and game.at_score < game.ht_score)
                )
                if is_lost and game.period_type in ("OT", "SO"):
                    losses_in_overtime += 1

        return { "total_as_favorite": total_as_favorite, "losses_in_overtime": losses_in_overtime }


async def get_overtime_and_shootout_results(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        wins_ot = 0
        losses_ot = 0
        wins_so = 0
        losses_so = 0

        for game, in games:
            is_home = game.hometeam == team_abbrev

            if game.period_type == "OT":
                if (is_home and game.ht_score > game.at_score) or (not is_home and game.at_score > game.ht_score):
                    wins_ot += 1
                else:
                    losses_ot += 1

            elif game.period_type == "SO":
                if (is_home and game.ht_score > game.at_score) or (not is_home and game.at_score > game.ht_score):
                    wins_so += 1
                else:
                    losses_so += 1

        return { "wins_ot": wins_ot, "losses_ot": losses_ot, "wins_so": wins_so, "losses_so": losses_so}