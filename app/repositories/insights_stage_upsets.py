# repositories/insights_stage_upsets.py

from app.models import Games, Quotes, Team
from app.crud import get_team_by_abbrev, get_playoff_teams, get_games_with_quotes_for_team
from sqlalchemy import select
from app.db import async_session
from app.utils.upset_rules import is_upset_relative
from collections import defaultdict

GAMETYPE_STAGE_MAP = {
    1: "preseason",
    2: "regular",
    3: "playoff"
}

async def get_stage_upsets_summary(threshold_diff=0.25):
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

            stage_totals = defaultdict(int)
            stage_upsets = defaultdict(int)

            for game, quote in rows:
                stage = GAMETYPE_STAGE_MAP.get(game.gametype, "unknown")

                opponent_abbrev = game.awayteam if game.hometeam == team_abbrev else game.hometeam
                opponent = await get_team_by_abbrev(session, opponent_abbrev)
                if not opponent:
                    continue

                tq, oq = (quote.quote_1, quote.quote_2) if quote.name_1 == team.name else (quote.quote_2, quote.quote_1)

                stage_totals[stage] += 1

                team_won = (
                    (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                    (game.awayteam == team_abbrev and game.at_score > game.ht_score)
                )

                if team_won and is_upset_relative(tq, oq, threshold_diff):
                    stage_upsets[stage] += 1

            result = {
                "team": team.name,
                "playoff": team_abbrev in playoff_teams
            }

            for stage in ["preseason", "regular", "playoff"]:
                total = stage_totals[stage]
                upsets = stage_upsets[stage]
                rate = round((upsets / total) * 100, 2) if total else 0
                result.update({
                    f"{stage}_games": total,
                    f"{stage}_upsets": upsets,
                    f"{stage}_rate": rate
                })

            results.append(result)

        return results