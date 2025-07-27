# app/repositories/upset_updater.py

from app.db import async_session
from app.models import Upset
from sqlalchemy import select, insert, update

from app.repositories.team_upset_repository import (
    get_team_upsets,
    get_team_upsets_by_stage,
    get_avg_upset_quote_for_team,
    get_team_upsets_with_quote_threshold,
    get_home_losses_as_favorite
)
from app.crud import get_total_games_by_team


async def update_team_upset(team_abbrev: str):
    async with async_session() as session:
        total_games = await get_total_games_by_team(session, team_abbrev)
        upsets = await get_team_upsets(team_abbrev)
        num_upsets = len(upsets)
        upset_share = round((num_upsets / total_games) * 100, 3) if total_games else 0

        avg_quote = await get_avg_upset_quote_for_team(team_abbrev)
        stage_data = await get_team_upsets_by_stage(team_abbrev)
        threshold_data = await get_team_upsets_with_quote_threshold(team_abbrev)
        home_data = await get_home_losses_as_favorite(team_abbrev)

        def safe_pct(num, denom):
            return round((num / denom) * 100, 3) if denom else 0

        data = {
            "team_abbrev": team_abbrev,
            "total_games": total_games,
            "num_upsets": num_upsets,
            "upset_share": upset_share,
            "avg_upset_quote": round(avg_quote, 3),

            "regular_total": stage_data["totals"].get("regular", 0),
            "regular_upsets": stage_data["upsets"].get("regular", 0),
            "preseason_total": stage_data["totals"].get("preseason", 0),
            "preseason_upsets": stage_data["upsets"].get("preseason", 0),
            "playoff_total": stage_data["totals"].get("playoff", 0),
            "playoff_upsets": stage_data["upsets"].get("playoff", 0),

            "total_games_with_high_quote": threshold_data["total_games_with_high_quote"],
            "upsets_with_high_quote": threshold_data["upsets_with_high_quote"],
            "share_with_high_quote": safe_pct(
                threshold_data["upsets_with_high_quote"],
                threshold_data["total_games_with_high_quote"]
            ),

            "total_home_games": home_data["total_home_games"],
            "home_fav_losses": home_data["home_fav_losses"],
            "home_loss_share": safe_pct(
                home_data["home_fav_losses"],
                home_data["total_home_games"]
            )
        }

        # Проверка существующей записи
        result = await session.execute(
            select(Upset).where(Upset.team_abbrev == team_abbrev)
        )
        existing = result.scalar_one_or_none()

        if existing:
            stmt = update(Upset).where(Upset.team_abbrev == team_abbrev).values(**data)
        else:
            stmt = insert(Upset).values(**data)

        await session.execute(stmt)
        await session.commit()