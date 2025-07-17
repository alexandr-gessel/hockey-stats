#repositories/team_correlation_analysis.py

from app.db import async_session
from app.crud import get_team_by_abbrev
from sqlalchemy import select, or_
from app.models import Games
from scipy.stats import pearsonr

async def get_correlation_metrics(team_abbrev: str):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            return {}

        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.scalars().all()

        if not games:
            return {}

        faceoff_win_in_wins = []
        faceoff_win_in_losses = []
        pim_in_wins = []
        pim_in_losses = []
        shots_list = []
        goals_list = []
        pp_conversion_wins = 0
        pp_conversion_total = 0

        for game in games:
            if game.hometeam == team_abbrev:
                goals = game.ht_score
                shots = game.ht_sog
                faceoff = game.ht_faceoffwinningpctg
                pim = game.ht_pim
                pp_conv = game.ht_powerplayconversion
                won = game.ht_score > game.at_score
            else:
                goals = game.at_score
                shots = game.at_sog
                faceoff = game.at_faceoffwinningpctg
                pim = game.at_pim
                pp_conv = game.at_powerplayconversion
                won = game.at_score > game.ht_score

            if faceoff is not None:
                if won:
                    faceoff_win_in_wins.append(faceoff)
                else:
                    faceoff_win_in_losses.append(faceoff)

            if pim is not None:
                if won:
                    pim_in_wins.append(pim)
                else:
                    pim_in_losses.append(pim)

            if shots is not None and goals is not None:
                shots_list.append(shots)
                goals_list.append(goals)

            if pp_conv and '/' in pp_conv:
                scored, attempts = map(int, pp_conv.split('/'))
                if attempts > 0:
                    pp_conversion_total += 1
                    if won and scored > 0:
                        pp_conversion_wins += 1

        def avg(lst):
            return sum(lst) / len(lst) if lst else 0

        shot_goal_corr = pearsonr(shots_list, goals_list)[0] if len(shots_list) > 2 else 0

        return {
            "faceoff_win_in_wins": round(avg(faceoff_win_in_wins), 2),
            "faceoff_win_in_losses": round(avg(faceoff_win_in_losses), 2),
            "pim_in_wins": round(avg(pim_in_wins), 2),
            "pim_in_losses": round(avg(pim_in_losses), 2),
            "shot_goal_corr": round(shot_goal_corr, 2),
            "pp_conversion_win_rate": round((pp_conversion_wins / pp_conversion_total) * 100, 2) if pp_conversion_total > 0 else 0
        }