# app/scripts/save_team_overtime_stats.py

import asyncio
from app.db import async_session
from app.crud import get_team_by_abbrev
from app.models import TeamOvertimeStats
from app.repositories.team_overtime_repository import (
    get_draws_in_regular_time,
    get_upset_wins_in_overtime,
    get_favorite_losses_in_overtime,
    get_overtime_and_shootout_results
)

async def save_overtime_stats(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Команда {team_abbrev} не найдена.")
            return

        draws = await get_draws_in_regular_time(team_abbrev)
        upset_ot = await get_upset_wins_in_overtime(team_abbrev)
        fav_losses = await get_favorite_losses_in_overtime(team_abbrev)
        ot_so = await get_overtime_and_shootout_results(team_abbrev)

        stats = TeamOvertimeStats(
            team_abbrev=team_abbrev,
            games_with_draw=draws["games_with_draw"],
            total_games=draws["total_games"],
            wins_in_overtime=upset_ot["wins_in_overtime"],
            total_as_underdog=upset_ot["total_as_underdog"],
            losses_in_overtime=fav_losses["losses_in_overtime"],
            total_as_favorite=fav_losses["total_as_favorite"],
            wins_ot=ot_so["wins_ot"],
            losses_ot=ot_so["losses_ot"],
            wins_so=ot_so["wins_so"],
            losses_so=ot_so["losses_so"]
        )

        await session.merge(stats)
        await session.commit()
        print(f"Сохранены данные по {team_abbrev}")

if __name__ == "__main__":
    asyncio.run(save_overtime_stats("MTL"))