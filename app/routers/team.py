# app/routers/team.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

from app.db import get_db
from app.crud import get_team_by_abbrev, get_total_games_by_team
from app.models import Team, TeamAnalytics, Upset, TeamOvertimeStats

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/team/{team_abbrev}")
async def read_team(team_abbrev: str, request: Request, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(
        select(Team, TeamAnalytics, Upset, TeamOvertimeStats)
        .join(TeamAnalytics, Team.abbrev == TeamAnalytics.team_abbrev)
        .join(Upset, Team.abbrev == Upset.team_abbrev)
        .join(TeamOvertimeStats, Team.abbrev == TeamOvertimeStats.team_abbrev)
        .where(Team.abbrev == team_abbrev)
    )
    record = result.one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Team nicht gefunden")

    team, analytics, upset, overtime = record

    draw_share = (overtime.games_with_draw / overtime.total_games * 100) if overtime.total_games > 0 else 0
    overtime_upset_share = (overtime.wins_in_overtime / overtime.total_as_underdog * 100) if overtime.total_as_underdog > 0 else 0
    favorite_overtime_loss_share = (overtime.losses_in_overtime / overtime.total_as_favorite * 100) if overtime.total_as_favorite > 0 else 0

    

    return templates.TemplateResponse("team.html", {
        "request": request,
        "team": team,
        "num_upsets": upset.num_upsets,
        "total_games": upset.total_games,
        "upset_share": round(upset.upset_share, 2),
        "stage_stats": {
            "regular_season_upsets": upset.regular_upsets,
            "playoff_upsets": upset.playoff_upsets
        },

        "avg_upset_quote": round(upset.avg_upset_quote, 2),
        
        "threshold_total": upset.total_games_with_high_quote,
        "threshold_upsets": upset.upsets_with_high_quote,
        "threshold_share": round(upset.share_with_high_quote, 2),
        "total_home_games": upset.total_games,
        "home_fav_losses": upset.home_fav_losses,
        "home_loss_share": round(upset.home_loss_share, 2),

        "total_games_draw": overtime.total_games,
        "games_with_draw": overtime.games_with_draw,
        "draw_share": round(draw_share, 2),
        "total_as_underdog": overtime.total_as_underdog,
        "wins_in_overtime": overtime.wins_in_overtime,
        "overtime_upset_share": round(overtime_upset_share, 2),
        "total_as_favorite": overtime.total_as_favorite,
        "losses_in_overtime": overtime.losses_in_overtime,
        "favorite_overtime_loss_share": round(favorite_overtime_loss_share, 2),
        "ot_so_results": {
            "wins_ot": overtime.wins_ot,
            "losses_ot": overtime.losses_ot,
            "wins_so": overtime.wins_so,
            "losses_so": overtime.losses_so
        },
        
        "bookmaker_analysis": { "expected_win_rate": round(upset.expected_win_rate, 2),
                                "real_win_rate": round(upset.real_win_rate, 2) },
        "max_upset_streak": upset.max_upset_streak,
        "max_fav_loss_streak": upset.max_fav_loss_streak,
        
        "game_summary": {
            "total_games": team.total_games,
            "wins": team.wins,
            "losses": team.losses,
            "draws": team.draws
        },
        "goal_stats": {
            "goals_for": team.goals_for,
            "goals_against": team.goals_against,
            "goal_diff": team.goal_diff,
            "avg_goals_for": round(team.avg_goals_for,2),
            "avg_goals_against": round(team.avg_goals_against,2)
        },
        "sog_stats": {
            "sog_for": team.sog_for,
            "sog_against": team.sog_against,
            "avg_sog_for": round(team.avg_sog_for, 2),
            "avg_sog_against": round(team.avg_sog_against,2)
        },
        "faceoff_stats": {
            "avg_faceoff_win_pct": round(team.avg_faceoff_win_pct,3)
        },
        "special_teams_stats": {
            "total_pp_goals": team.total_pp_goals,
            "total_pp_attempts": team.total_pp_attempts,
            "powerplay_pct": round(team.powerplay_pct, 2),
            "total_pim": team.total_pim,
            "avg_pim_per_game": round(team.avg_pim_per_game,2)
        },
        "hits_blocks_stats": {
            "total_hits": team.total_hits,
            "total_blocks": team.total_blocks,
            "avg_hits": round(team.avg_hits, 2),
            "avg_blocks": round(team.avg_blocks,2)
        },
        "streaks": {
            "max_win_streak": team.max_win_streak,
            "max_loss_streak": team.max_loss_streak
        },
        "home_away_stats": {
            "home_wins": team.home_wins,
            "home_losses": team.home_losses,
            "away_wins": team.away_wins,
            "away_losses": team.away_losses
        },
        
        "correlation_metrics": {
            "faceoff_win_in_wins": round(analytics.faceoff_win_in_wins, 2),
            "faceoff_win_in_losses": round(analytics.faceoff_win_in_losses,2),
            "pim_in_wins": round(analytics.pim_in_wins, 2),
            "pim_in_losses": round(analytics.pim_in_losses, 2),
            "shot_goal_corr": round(analytics.shot_goal_corr, 2),
            "pp_conversion_win_rate": round(analytics.pp_conversion_win_rate,2)
        },

        "advanced_ratios": {
            "shot_conversion": analytics.shot_conversion,
            "faceoff_win_impact": analytics.faceoff_win_impact,
            "hit_to_goal": round(analytics.hit_to_goal, 2),
            "block_to_shot": analytics.block_to_shot
        }
    })