# repositories/insights_home_upsets.py

from app.models import Games, Quotes, Team
from app.crud import get_team_by_abbrev, get_playoff_teams, get_games_with_quotes_for_team
from sqlalchemy import select
from app.db import async_session
from app.utils.upset_rules import is_upset_relative

async def get_home_upsets_summary(threshold_diff=0.25):
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

            total_home_games = 0
            home_upsets = 0

            for game, quote in rows:
                if game.hometeam != team_abbrev:
                    continue

                opponent = await get_team_by_abbrev(session, game.awayteam)
                if not opponent:
                    continue

                tq, oq = (quote.quote_1, quote.quote_2) if quote.name_1 == team.name else (quote.quote_2, quote.quote_1)

                total_home_games += 1

                if game.ht_score > game.at_score and is_upset_relative(tq, oq, threshold_diff):
                    home_upsets += 1

            upset_rate = round((home_upsets / total_home_games) * 100, 2) if total_home_games else 0

            results.append({
                "team": team.name,
                "home_games_played": total_home_games,
                "home_upsets": home_upsets,
                "home_upset_rate": upset_rate,
                "playoff": team_abbrev in playoff_teams
            })

        return results