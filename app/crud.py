#app/crud.py

from sqlalchemy.future import select
from sqlalchemy import or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.models import Team, Games, Quotes, GoalsByPeriod

async def get_teams(db: AsyncSession):
    result = await db.execute(select(Team).order_by(Team.abbrev))
    return result.scalars().all()

async def get_team_by_abbrev(db: AsyncSession, abbrev: str):
    result = await db.execute(select(Team).where(Team.abbrev == abbrev))
    return result.scalars().first()

async def get_teams_grouped_by_division(db: AsyncSession):
    result = await db.execute(select(Team))
    teams = result.scalars().all()
    
    divisions = {}
    for team in teams:
        division = team.division
        if division not in divisions:
            divisions[division] = []
        divisions[division].append({"name": team.name, "abbr": team.abbrev})
    
    return divisions

async def get_all_teams_stats(db: AsyncSession):
    result = await db.execute(select(Team))
    return result.scalars().all()


async def get_total_games_by_team(db: AsyncSession, team_abbrev: str) -> int:
    result = await db.execute(
        select(Games).where(
            or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
        )
    )
    games = result.scalars().all()
    return len(games)


async def get_games_with_quotes_for_team(db: AsyncSession, team_full_name: str, team_abbrev: str):
    result = await db.execute(
        select(Games, Quotes).join(
            Quotes,
            and_(
                Quotes.spieldate.between(Games.gamedate - timedelta(days=1), Games.gamedate + timedelta(days=1)),
                or_(
                    Quotes.name_1 == team_full_name,
                    Quotes.name_2 == team_full_name
                )
            )
        ).where(
            or_(
                Games.hometeam == team_abbrev,
                Games.awayteam == team_abbrev
            )
        )
    )
    return result.fetchall()

async def get_game_by_id(db, game_id: int):
    result = await db.execute(select(Games).where(Games.id_game == game_id))
    return result.scalar_one_or_none()

async def get_playoff_teams(db: AsyncSession) -> set:
    result = await db.execute(
        select(Games.hometeam, Games.awayteam).where(Games.id_game >= 2021030001)
    )
    rows = result.all()

    playoff_teams = set()
    for home, away in rows:
        playoff_teams.add(home)
        playoff_teams.add(away)

    return playoff_teams


async def get_goals_by_game_id(db: AsyncSession, game_id: int) -> GoalsByPeriod | None:
    result = await db.execute(
        select(GoalsByPeriod).where(GoalsByPeriod.id_game == game_id)
    )
    return result.scalars().first()