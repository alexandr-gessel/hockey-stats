# repositories/insights_upset_streaks.py

from app.models import Games, Quotes, Team
from app.crud import get_team_by_abbrev, get_playoff_teams, get_games_with_quotes_for_team
from sqlalchemy import select
from app.db import async_session
from app.utils.upset_rules import is_upset_relative

async def get_upset_streaks_summary(threshold_diff=0.25):
    async with async_session() as session:
        teams_result = await session.execute(select(Team.abbrev))
        teams_data = teams_result.scalars().all()

        playoff_teams = await get_playoff_teams(session)

        results = []

        for team_abbrev in teams_data:
            team = await get_team_by_abbrev(session, team_abbrev)
            if not team:
                continue

            rows = await get_games_with_quotes_for_team(session, team.name, team_abbrev)

            # Сортируем по дате
            rows_sorted = sorted(rows, key=lambda row: row[0].gamedate)

            max_streak = 0
            current_streak = 0

            for game, quote in rows_sorted:
                opponent_abbrev = game.awayteam if game.hometeam == team_abbrev else game.hometeam
                opponent = await get_team_by_abbrev(session, opponent_abbrev)
                if not opponent:
                    continue

                tq, oq = (quote.quote_1, quote.quote_2) if quote.name_1 == team.name else (quote.quote_2, quote.quote_1)

                team_won = (
                    (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                    (game.awayteam == team_abbrev and game.at_score > game.ht_score)
                )

                if team_won and is_upset_relative(tq, oq, threshold_diff):
                    current_streak += 1
                    max_streak = max(max_streak, current_streak)
                else:
                    current_streak = 0

            results.append({
                "team": team.name,
                "max_upset_streak": max_streak,
                "playoff": team_abbrev in playoff_teams
            })

        return results