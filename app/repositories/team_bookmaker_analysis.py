# repositories/team_bookmaker_analysis.py

from app.utils.upset_rules import is_upset_relative
from app.db import async_session
from app.crud import get_team_by_abbrev
from sqlalchemy import select, or_, and_
from app.models import Games, Quotes
from datetime import timedelta
from app.utils.bookmaker_tools import corrected_probability_3way

async def get_bookmaker_error_estimation(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return {"avg_expected_win": 0, "real_win_rate": 0, "total_games": 0}

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

        total_games = 0
        total_expected_win = 0
        total_real_wins = 0

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

            # Используем корректированную вероятность для 3 исходов
            expected_win_prob = corrected_probability_3way(team_quote, quote.quote_un, opponent_quote)

            is_winner = (
                (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                (game.awayteam == team_abbrev and game.at_score > game.ht_score)
            )

            total_games += 1
            total_expected_win += expected_win_prob

            if is_winner:
                total_real_wins += 1

        avg_expected_win = (total_expected_win / total_games) if total_games > 0 else 0
        real_win_rate = (total_real_wins / total_games) if total_games > 0 else 0

        return {
            "avg_expected_win": round(avg_expected_win * 100, 2),
            "real_win_rate": round(real_win_rate * 100, 2),
            "total_games": total_games
        }

