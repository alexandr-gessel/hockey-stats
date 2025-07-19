# app/ingest/aggregate_goalies_summary.py

from sqlalchemy import select, func, Integer, case, text
from app.db import async_session
from app.models import Goalies, GoaliesSummary


def parse_shots_expression(expr):
    """PostgreSQL expression to extract first number in '8/10'."""
    return func.coalesce(
        func.cast(func.split_part(expr, '/', 1), Integer),
        0
    )


async def aggregate_goalies_summary():
    async with async_session() as session:
        await session.execute(text('TRUNCATE TABLE goalies_summary'))

        result = await session.execute(
            select(
                Goalies.playerid,
                func.min(Goalies.name).label("name"),
                func.count(Goalies.id).label("games_played"),
                func.sum(parse_shots_expression(Goalies.evenstrengthshotsagainst)).label("evenstrengthshotsagainst"),
                func.sum(parse_shots_expression(Goalies.powerplayshotsagainst)).label("powerplayshotsagainst"),
                func.sum(parse_shots_expression(Goalies.shorthandedshotsagainst)).label("shorthandedshotsagainst"),
                func.sum(parse_shots_expression(Goalies.saveshotsagainst)).label("saveshotsagainst"),
                func.avg(Goalies.savepctg).label("savepctg"),
                func.sum(Goalies.evenstrengthgoalsagainst).label("evenstrengthgoalsagainst"),
                func.sum(Goalies.powerplaygoalsagainst).label("powerplaygoalsagainst"),
                func.sum(Goalies.shorthandedgoalsagainst).label("shorthandedgoalsagainst"),
                func.sum(Goalies.goalsagainst).label("goalsagainst"),
                func.sum(Goalies.pim).label("pim"),
                func.sum(
                    case(
                        (func.length(Goalies.toi) > 0,
                         func.cast(func.split_part(Goalies.toi, ':', 1), Integer) * 60 +
                         func.cast(func.split_part(Goalies.toi, ':', 2), Integer)
                         ),
                        else_=0
                    )
                ).label("toi_total")
            ).group_by(Goalies.playerid)
        )

        rows = result.all()

        for row in rows:
            summary = GoaliesSummary(
                playerid=row.playerid,
                name=row.name,
                games_played=row.games_played,
                evenstrengthshotsagainst=row.evenstrengthshotsagainst or 0,
                powerplayshotsagainst=row.powerplayshotsagainst or 0,
                shorthandedshotsagainst=row.shorthandedshotsagainst or 0,
                saveshotsagainst=row.saveshotsagainst or 0,
                savepctg=row.savepctg or 0.0,
                evenstrengthgoalsagainst=row.evenstrengthgoalsagainst or 0,
                powerplaygoalsagainst=row.powerplaygoalsagainst or 0,
                shorthandedgoalsagainst=row.shorthandedgoalsagainst or 0,
                goalsagainst=row.goalsagainst or 0,
                pim=row.pim or 0,
                toi_total=row.toi_total or 0
            )
            session.add(summary)

        await session.commit()