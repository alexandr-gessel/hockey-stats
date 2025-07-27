# app/scripts/save_all_upset_stats_extended.py

import asyncio
from app.db import async_session
from app.models import Upset
from app.crud import get_teams
from app.repositories.team_bookmaker_analysis import get_bookmaker_error_estimation
from app.repositories.team_upset_streaks import get_max_upset_streak, get_max_fav_loss_streak

async def save_extended_upset_stats():
    async with async_session() as session:
        teams = await get_teams(session)

        for team in teams:
            team_abbrev = team.abbrev
            print(f" abarbeitet : {team_abbrev}")

            
            result = await session.execute(
                Upset.__table__.select().where(Upset.team_abbrev == team_abbrev)
            )
            row = result.fetchone()
            if not row:
                print(f"keine Info {team_abbrev} in upset")
                continue

            
            bookmaker_data = await get_bookmaker_error_estimation(team_abbrev)
            max_upset = await get_max_upset_streak(team_abbrev)
            max_fav_loss = await get_max_fav_loss_streak(team_abbrev)

           
            await session.execute(
                Upset.__table__.update()
                .where(Upset.team_abbrev == team_abbrev)
                .values(
                    real_win_rate=bookmaker_data["real_win_rate"],
                    expected_win_rate=bookmaker_data["avg_expected_win"],
                    max_upset_streak=max_upset,
                    max_fav_loss_streak=max_fav_loss,
                )
            )
            print(f" UPD for {team_abbrev}")

        await session.commit()
        print("getun")

if __name__ == "__main__":
    asyncio.run(save_extended_upset_stats())