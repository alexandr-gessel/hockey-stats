# repositories/insights_analysis.py

from app.models import Games, Quotes, Team
from app.crud import get_team_by_abbrev, get_playoff_teams, get_games_with_quotes_for_team
from sqlalchemy import select
from app.db import async_session
from app.utils.upset_rules import is_upset_relative

from app.models import Games, Quotes, Team
from app.crud import get_team_by_abbrev, get_playoff_teams, get_games_with_quotes_for_team
from sqlalchemy import select
from app.db import async_session
from app.utils.upset_rules import is_upset_relative

async def get_team_upsets_summary(threshold_diff=0.25):
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

            total_games = 0
            upset_games = 0

            for game, quote in rows:
                opponent_abbrev = game.awayteam if game.hometeam == team_abbrev else game.hometeam
                opponent = await get_team_by_abbrev(session, opponent_abbrev)
                if not opponent:
                    continue

                tq, oq = (quote.quote_1, quote.quote_2) if quote.name_1 == team.name else (quote.quote_2, quote.quote_1)

                # Считаем ВСЕ игры с котировками
                total_games += 1

                team_won = (
                    (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                    (game.awayteam == team_abbrev and game.at_score > game.ht_score)
                )

                if team_won and is_upset_relative(tq, oq, threshold_diff):
                    upset_games += 1

            upset_rate = round((upset_games / total_games) * 100, 2) if total_games else 0

            results.append({
                "team": team.name,
                "games_played": total_games,
                "upsets": upset_games,
                "upset_rate": upset_rate,
                "playoff": team_abbrev in playoff_teams
            })

        return results