# app/repositories/team_analytics_updater.py

from app.db import async_session
from app.models import TeamAnalytics
from sqlalchemy import select, insert, update

from app.repositories.team_correlation_analysis import get_correlation_metrics
from app.repositories.team_advanced_ratios import get_advanced_ratios

async def update_team_analytics(team_abbrev: str):
    correlation = await get_correlation_metrics(team_abbrev)
    advanced = await get_advanced_ratios(team_abbrev)

    async with async_session() as session:
        result = await session.execute(
            select(TeamAnalytics).where(TeamAnalytics.team_abbrev == team_abbrev)
        )
        existing = result.scalar_one_or_none()

        if existing:
            stmt = (
                update(TeamAnalytics)
                .where(TeamAnalytics.team_abbrev == team_abbrev)
                .values(
                    faceoff_win_in_wins=round(correlation.get("faceoff_win_in_wins", 0), 3),
                    faceoff_win_in_losses=round(correlation.get("faceoff_win_in_losses", 0), 3),
                    pim_in_wins=round(correlation.get("pim_in_wins", 0), 3),
                    pim_in_losses=round(correlation.get("pim_in_losses", 0), 3),
                    shot_goal_corr=round(correlation.get("shot_goal_corr", 0), 3),
                    pp_conversion_win_rate=round(correlation.get("pp_conversion_win_rate", 0), 3),

                    shot_conversion=round(advanced.get("shot_conversion", 0), 3),
                    faceoff_win_impact=round(advanced.get("faceoff_win_impact", 0), 3),
                    hit_to_goal=round(advanced.get("hit_to_goal", 0), 3),
                    block_to_shot=round(advanced.get("block_to_shot", 0), 3),
                )
            )
            await session.execute(stmt)
        else:
            stmt = insert(TeamAnalytics).values(
                team_abbrev=team_abbrev,
                faceoff_win_in_wins=round(correlation.get("faceoff_win_in_wins", 0), 3),
                faceoff_win_in_losses=round(correlation.get("faceoff_win_in_losses", 0), 3),
                pim_in_wins=round(correlation.get("pim_in_wins", 0), 3),
                pim_in_losses=round(correlation.get("pim_in_losses", 0), 3),
                shot_goal_corr=round(correlation.get("shot_goal_corr", 0), 3),
                pp_conversion_win_rate=round(correlation.get("pp_conversion_win_rate", 0), 3),

                shot_conversion=round(advanced.get("shot_conversion", 0), 3),
                faceoff_win_impact=round(advanced.get("faceoff_win_impact", 0), 3),
                hit_to_goal=round(advanced.get("hit_to_goal", 0), 3),
                block_to_shot=round(advanced.get("block_to_shot", 0), 3),
            )
            await session.execute(stmt)

        await session.commit()