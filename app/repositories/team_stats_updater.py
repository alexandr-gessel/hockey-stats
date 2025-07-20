# app/repositories/team_stats_updater.py

from app.db import async_session
from app.models import Team
from sqlalchemy import update

from app.repositories.team_summary_repository import (
    get_team_game_summary,
    get_team_goal_stats,
    get_team_sog_stats,
    get_team_faceoff_stats,
    get_team_special_teams_stats,
    get_team_hits_blocks_stats,
    get_team_streaks,
    get_team_home_away_stats
)

async def update_team_stats(team_abbrev: str):
    async with async_session() as session:
        game_summary = await get_team_game_summary(team_abbrev)
        goal_stats = await get_team_goal_stats(team_abbrev)
        sog_stats = await get_team_sog_stats(team_abbrev)
        faceoff_stats = await get_team_faceoff_stats(team_abbrev)
        special_teams_stats = await get_team_special_teams_stats(team_abbrev)
        hits_blocks_stats = await get_team_hits_blocks_stats(team_abbrev)
        streaks = await get_team_streaks(team_abbrev)
        home_away_stats = await get_team_home_away_stats(team_abbrev)

        stmt = (
            update(Team)
            .where(Team.abbrev == team_abbrev)
            .values(
                total_games=game_summary["total_games"],
                wins=game_summary["wins"],
                losses=game_summary["losses"],
                draws=game_summary["draws"],

                goals_for=goal_stats["goals_for"],
                goals_against=goal_stats["goals_against"],
                goal_diff=goal_stats["goal_diff"],
                avg_goals_for=round(goal_stats["avg_goals_for"], 3),
                avg_goals_against=round(goal_stats["avg_goals_against"], 3),

                sog_for=sog_stats["sog_for"],
                sog_against=sog_stats["sog_against"],
                avg_sog_for=round(sog_stats["avg_sog_for"], 3),
                avg_sog_against=round(sog_stats["avg_sog_against"], 3),

                avg_faceoff_win_pct=round(faceoff_stats["avg_faceoff_win_pct"], 3),

                total_pp_goals=special_teams_stats["total_pp_goals"],
                total_pp_attempts=special_teams_stats["total_pp_attempts"],
                powerplay_pct=round(special_teams_stats["powerplay_pct"], 3),
                total_pim=special_teams_stats["total_pim"],
                avg_pim_per_game=round(special_teams_stats["avg_pim_per_game"], 3),

                total_hits=hits_blocks_stats["total_hits"],
                total_blocks=hits_blocks_stats["total_blocks"],
                avg_hits=round(hits_blocks_stats["avg_hits"], 3),
                avg_blocks=round(hits_blocks_stats["avg_blocks"], 3),

                max_win_streak=streaks["max_win_streak"],
                max_loss_streak=streaks["max_loss_streak"],

                home_wins=home_away_stats["home_wins"],
                home_losses=home_away_stats["home_losses"],
                away_wins=home_away_stats["away_wins"],
                away_losses=home_away_stats["away_losses"],
            )
        )

        await session.execute(stmt)
        await session.commit()