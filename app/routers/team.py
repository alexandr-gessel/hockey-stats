# app/routers/team.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.crud import get_team_by_abbrev, get_total_games_by_team
from app.models import TeamAnalytics

from app.repositories.team_upset_repository import (
    get_team_upsets, get_team_upsets_by_stage, get_avg_upset_quote_for_team,
    get_team_upsets_with_quote_threshold, get_home_losses_as_favorite
)
from app.repositories.team_overtime_repository import (
    get_draws_in_regular_time, get_upset_wins_in_overtime,
    get_favorite_losses_in_overtime, get_overtime_and_shootout_results
)
from app.repositories.team_bookmaker_analysis import get_bookmaker_error_estimation
from app.repositories.team_upset_streaks import get_max_upset_streak, get_max_fav_loss_streak


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/team/{team_abbrev}")
async def read_team(team_abbrev: str, request: Request, db: AsyncSession = Depends(get_db)):
    team = await get_team_by_abbrev(db, team_abbrev.upper())
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    result = await db.execute(
        select(TeamAnalytics).where(TeamAnalytics.team_abbrev == team_abbrev)
    )
    analytics = result.scalar_one_or_none()
    if not analytics:
        raise HTTPException(status_code=404, detail="Team analytics not found")


    upsets = await get_team_upsets(team_abbrev)
    num_upsets = len(upsets)
    total_games = await get_total_games_by_team(db, team_abbrev)
    upset_share = (num_upsets / total_games * 100) if total_games > 0 else 0

    stage_stats = await get_team_upsets_by_stage(team_abbrev)
    avg_upset_quote = await get_avg_upset_quote_for_team(team_abbrev)

    threshold_data = await get_team_upsets_with_quote_threshold(team_abbrev, quote_threshold=2.50)
    threshold_total = threshold_data["total_games_with_high_quote"]
    threshold_upsets = threshold_data["upsets_with_high_quote"]
    threshold_share = (threshold_upsets / threshold_total * 100) if threshold_total > 0 else 0

    home_loss_data = await get_home_losses_as_favorite(team_abbrev)
    total_home_games = home_loss_data["total_home_games"]
    home_fav_losses = home_loss_data["home_fav_losses"]
    home_loss_share = (home_fav_losses / total_home_games * 100) if total_home_games > 0 else 0

    draw_data = await get_draws_in_regular_time(team_abbrev)
    total_games_draw = draw_data["total_games"]
    games_with_draw = draw_data["games_with_draw"]
    draw_share = (games_with_draw / total_games_draw * 100) if total_games_draw > 0 else 0

    overtime_upset_data = await get_upset_wins_in_overtime(team_abbrev)
    total_as_underdog = overtime_upset_data["total_as_underdog"]
    wins_in_overtime = overtime_upset_data["wins_in_overtime"]
    overtime_upset_share = (wins_in_overtime / total_as_underdog * 100) if total_as_underdog > 0 else 0

    favorite_overtime_data = await get_favorite_losses_in_overtime(team_abbrev)
    total_as_favorite = favorite_overtime_data["total_as_favorite"]
    losses_in_overtime = favorite_overtime_data["losses_in_overtime"]
    favorite_overtime_loss_share = (losses_in_overtime / total_as_favorite * 100) if total_as_favorite > 0 else 0

    ot_so_results = await get_overtime_and_shootout_results(team_abbrev)
    bookmaker_analysis = await get_bookmaker_error_estimation(team_abbrev)
    max_upset_streak = await get_max_upset_streak(team_abbrev)
    max_fav_loss_streak = await get_max_fav_loss_streak(team_abbrev)

    

    return templates.TemplateResponse("team.html", {
        "request": request,
        "team": team,
        "num_upsets": num_upsets,
        "total_games": total_games,
        "upset_share": round(upset_share, 2),
        "stage_stats": stage_stats,
        "avg_upset_quote": avg_upset_quote,
        "threshold_total": threshold_total,
        "threshold_upsets": threshold_upsets,
        "threshold_share": round(threshold_share, 2),
        "total_home_games": total_home_games,
        "home_fav_losses": home_fav_losses,
        "home_loss_share": round(home_loss_share, 2),
        "total_games_draw": total_games_draw,
        "games_with_draw": games_with_draw,
        "draw_share": round(draw_share, 2),
        "total_as_underdog": total_as_underdog,
        "wins_in_overtime": wins_in_overtime,
        "overtime_upset_share": round(overtime_upset_share, 2),
        "total_as_favorite": total_as_favorite,
        "losses_in_overtime": losses_in_overtime,
        "favorite_overtime_loss_share": round(favorite_overtime_loss_share, 2),
        "ot_so_results": ot_so_results,
        "bookmaker_analysis": bookmaker_analysis,
        "max_upset_streak": max_upset_streak,
        "max_fav_loss_streak": max_fav_loss_streak,
        
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