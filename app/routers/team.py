# app/routers/team.py

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud import get_team_by_abbrev, get_total_games_by_team
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
from app.repositories.team_summary_repository import (
    get_team_game_summary, get_team_goal_stats, get_team_sog_stats,
    get_team_faceoff_stats, get_team_special_teams_stats, get_team_hits_blocks_stats,
    get_team_streaks, get_team_home_away_stats
)
from app.repositories.team_correlation_analysis import get_correlation_metrics
from app.repositories.team_advanced_ratios import get_advanced_ratios

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/team/{team_abbrev}")
async def read_team(team_abbrev: str, request: Request, db: AsyncSession = Depends(get_db)):
    team = await get_team_by_abbrev(db, team_abbrev.upper())
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

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

    game_summary = await get_team_game_summary(team_abbrev)
    goal_stats = await get_team_goal_stats(team_abbrev)
    sog_stats = await get_team_sog_stats(team_abbrev)
    faceoff_stats = await get_team_faceoff_stats(team_abbrev)
    special_teams_stats = await get_team_special_teams_stats(team_abbrev)
    hits_blocks_stats = await get_team_hits_blocks_stats(team_abbrev)
    streaks = await get_team_streaks(team_abbrev)
    home_away_stats = await get_team_home_away_stats(team_abbrev)
    correlation_metrics = await get_correlation_metrics(team_abbrev)
    advanced_ratios = await get_advanced_ratios(team_abbrev)

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
        "game_summary": game_summary,
        "goal_stats": goal_stats,
        "sog_stats": sog_stats,
        "faceoff_stats": faceoff_stats,
        "special_teams_stats": special_teams_stats,
        "hits_blocks_stats": hits_blocks_stats,
        "streaks": streaks,
        "home_away_stats": home_away_stats,
        "correlation_metrics": correlation_metrics,
        "advanced_ratios": advanced_ratios
    })