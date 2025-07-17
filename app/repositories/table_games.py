# repositories/table_games.py 

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Games
from collections import defaultdict


def parse_pp_conversion(pp_string: str | None) -> float | None:
    if not pp_string or '/' not in pp_string:
        return None
    try:
        scored, attempts = map(int, pp_string.split('/'))
        if attempts == 0:
            return 0.0
        return round((scored / attempts) * 100, 2)
    except Exception:
        return None


async def get_teams_stats(db: AsyncSession):
    stmt_home = select(
        Games.hometeam.label('team'),
        func.count().label('games_played'),
        func.sum(Games.ht_score).label('goals_for'),
        func.sum(Games.at_score).label('goals_against'),
        func.sum(Games.ht_sog).label('sog_for'),
        func.sum(Games.at_sog).label('sog_against'),
        func.avg(Games.ht_faceoffwinningpctg).label('faceoff_pct'),
        func.sum(Games.ht_pim).label('pim'),
        func.sum(Games.ht_hits).label('hits'),
        func.sum(Games.ht_blocks).label('blocks'),
        func.sum(case((Games.ht_score > Games.at_score, 1), else_=0)).label('wins'),
        func.sum(case((Games.ht_score < Games.at_score, 1), else_=0)).label('losses'),
        func.sum(case((Games.ht_score == Games.at_score, 1), else_=0)).label('ties'),
        Games.ht_powerplayconversion.label('pp_raw')
    ).group_by(Games.hometeam, Games.ht_powerplayconversion)

    stmt_away = select(
        Games.awayteam.label('team'),
        func.count().label('games_played'),
        func.sum(Games.at_score).label('goals_for'),
        func.sum(Games.ht_score).label('goals_against'),
        func.sum(Games.at_sog).label('sog_for'),
        func.sum(Games.ht_sog).label('sog_against'),
        func.avg(Games.at_faceoffwinningpctg).label('faceoff_pct'),
        func.sum(Games.at_pim).label('pim'),
        func.sum(Games.at_hits).label('hits'),
        func.sum(Games.at_blocks).label('blocks'),
        func.sum(case((Games.at_score > Games.ht_score, 1), else_=0)).label('wins'),
        func.sum(case((Games.at_score < Games.ht_score, 1), else_=0)).label('losses'),
        func.sum(case((Games.at_score == Games.ht_score, 1), else_=0)).label('ties'),
        Games.at_powerplayconversion.label('pp_raw')
    ).group_by(Games.awayteam, Games.at_powerplayconversion)

    home_result = await db.execute(stmt_home)
    away_result = await db.execute(stmt_away)

    stats = defaultdict(lambda: {
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "goals_for": 0,
        "goals_against": 0,
        "sog_for": 0,
        "sog_against": 0,
        "faceoff_pct_sum": 0.0,
        "faceoff_pct_count": 0,
        "pp_pct_sum": 0.0,
        "pp_pct_count": 0,
        "pim": 0,
        "hits": 0,
        "blocks": 0,
    })

    def aggregate_row(row):
        team = row.team
        s = stats[team]
        s["games_played"] += row.games_played
        s["wins"] += row.wins
        s["losses"] += row.losses
        s["ties"] += row.ties
        s["goals_for"] += row.goals_for
        s["goals_against"] += row.goals_against
        s["sog_for"] += row.sog_for
        s["sog_against"] += row.sog_against
        if row.faceoff_pct is not None:
            s["faceoff_pct_sum"] += float(row.faceoff_pct)
            s["faceoff_pct_count"] += 1
        if row.pp_raw:
            parsed_pp = parse_pp_conversion(row.pp_raw)
            if parsed_pp is not None:
                s["pp_pct_sum"] += parsed_pp
                s["pp_pct_count"] += 1
        s["pim"] += row.pim
        s["hits"] += row.hits
        s["blocks"] += row.blocks

    for row in home_result.fetchall():
        aggregate_row(row)
    for row in away_result.fetchall():
        aggregate_row(row)

    result = []
    for team, s in stats.items():
        result.append({
            "abbr": team,
            "games_played": s["games_played"],
            "wins": s["wins"],
            "losses": s["losses"],
            "ties": s["ties"],
            "goals_for": s["goals_for"],
            "goals_against": s["goals_against"],
            "sog_for": s["sog_for"],
            "sog_against": s["sog_against"],
            "faceoff_pct": round(s["faceoff_pct_sum"] / s["faceoff_pct_count"], 2) if s["faceoff_pct_count"] > 0 else 0,
            "pp_pct": round(s["pp_pct_sum"] / s["pp_pct_count"], 2) if s["pp_pct_count"] > 0 else 0,
            "pim": s["pim"],
            "hits": s["hits"],
            "blocks": s["blocks"],
            "goal_diff": s["goals_for"] - s["goals_against"]
        })

    return result