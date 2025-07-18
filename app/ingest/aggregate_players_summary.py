# ingest/aggregate_players_summary.py

from sqlalchemy import select, func, Integer, case, text
from app.db import async_session
from app.models import ForwardsDefense
from app.models import PlayersSummary

async def aggregate_players_summary():
    async with async_session() as session:
        await session.execute(text('TRUNCATE TABLE players_summary'))

        result = await session.execute(
            select(
                ForwardsDefense.playerid,
                func.min(ForwardsDefense.name).label("name"),
                func.min(ForwardsDefense.position).label("position"),
                func.count(ForwardsDefense.id).label("games_played"),
                func.sum(ForwardsDefense.goals).label("goals"),
                func.sum(ForwardsDefense.assists).label("assists"),
                func.sum(ForwardsDefense.points).label("points"),
                func.sum(ForwardsDefense.plusminus).label("plusminus"),
                func.sum(ForwardsDefense.hits).label("hits"),
                func.sum(ForwardsDefense.blockedshots).label("blockedshots"),
                func.sum(ForwardsDefense.pim).label("pim"),
                func.sum(ForwardsDefense.shots).label("shots"),
                func.sum(
                    func.coalesce(
                        func.cast(func.split_part(ForwardsDefense.faceoffs, '/', 2), Integer),
                        0
                    )
                ).label("faceoffs"),
                func.avg(ForwardsDefense.faceoffwinningpctg).label("faceoffwinningpctg"),
                func.sum(
                    func.coalesce(
                        case(
                            (func.length(ForwardsDefense.toi) > 0,
                             func.cast(func.split_part(ForwardsDefense.toi, ':', 1), Integer) * 60 +
                             func.cast(func.split_part(ForwardsDefense.toi, ':', 2), Integer)
                             ),
                            else_=0
                        ),
                        0
                    )
                ).label("toi_total")
            ).group_by(
                ForwardsDefense.playerid
            )
        )

        rows = result.all()

        for row in rows:
            summary = PlayersSummary(
                playerid=row.playerid,
                name=row.name,
                position=row.position,
                games_played=row.games_played,
                goals=row.goals or 0,
                assists=row.assists or 0,
                points=row.points or 0,
                plusminus=row.plusminus or 0,
                hits=row.hits or 0,
                blockedshots=row.blockedshots or 0,
                pim=row.pim or 0,
                shots=row.shots or 0,
                faceoffs=row.faceoffs or 0,
                faceoffwinningpctg=row.faceoffwinningpctg or 0.0,
                toi_total=row.toi_total or 0
            )
            session.add(summary)

        await session.commit()