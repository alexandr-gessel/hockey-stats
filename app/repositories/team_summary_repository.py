# repositories/team_summary_repository.py

from sqlalchemy import select, or_
from app.db import async_session
from app.models import Games

async def get_team_game_summary(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_games = 0
        wins = 0
        losses = 0
        draws = 0  # игры, завершившиеся вничью в основное время

        for game, in games:
            total_games += 1

            if game.hometeam == team_abbrev and game.ht_score > game.at_score:
                wins += 1
            elif game.awayteam == team_abbrev and game.at_score > game.ht_score:
                wins += 1
            elif game.period_number > 3:
                draws += 1
            else:
                losses += 1

        return {
            "total_games": total_games,
            "wins": wins,
            "losses": losses,
            "draws": draws
        }

async def get_team_goal_stats(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_games = 0
        goals_for = 0
        goals_against = 0

        for game, in games:
            total_games += 1

            if game.hometeam == team_abbrev:
                goals_for += game.ht_score
                goals_against += game.at_score
            else:
                goals_for += game.at_score
                goals_against += game.ht_score

        avg_goals_for = (goals_for / total_games) if total_games > 0 else 0
        avg_goals_against = (goals_against / total_games) if total_games > 0 else 0
        goal_diff = goals_for - goals_against

        return {
            "total_games": total_games,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_diff": goal_diff,
            "avg_goals_for": round(avg_goals_for, 2),
            "avg_goals_against": round(avg_goals_against, 2)
        }

async def get_team_sog_stats(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_games = 0
        sog_for = 0
        sog_against = 0

        for game, in games:
            total_games += 1

            if game.hometeam == team_abbrev:
                sog_for += game.ht_sog
                sog_against += game.at_sog
            else:
                sog_for += game.at_sog
                sog_against += game.ht_sog

        avg_sog_for = (sog_for / total_games) if total_games > 0 else 0
        avg_sog_against = (sog_against / total_games) if total_games > 0 else 0

        return {
            "total_games": total_games,
            "sog_for": sog_for,
            "sog_against": sog_against,
            "avg_sog_for": round(avg_sog_for, 2),
            "avg_sog_against": round(avg_sog_against, 2)
        }

async def get_team_faceoff_stats(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_games = 0
        total_pct = 0

        for game, in games:
            if game.hometeam == team_abbrev and game.ht_faceoffwinningpctg is not None:
                total_pct += game.ht_faceoffwinningpctg
                total_games += 1
            elif game.awayteam == team_abbrev and game.at_faceoffwinningpctg is not None:
                total_pct += game.at_faceoffwinningpctg
                total_games += 1

        avg_pct = (total_pct / total_games) if total_games > 0 else 0

        return {
            "total_games": total_games,
            "avg_faceoff_win_pct": round(avg_pct, 2)
        }

async def get_team_special_teams_stats(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_pp_goals = 0
        total_pp_attempts = 0
        total_pim = 0
        total_games = 0

        for game, in games:
            if game.hometeam == team_abbrev:
                if game.ht_powerplayconversion:
                    try:
                        goals, attempts = map(int, game.ht_powerplayconversion.split('/'))
                        total_pp_goals += goals
                        total_pp_attempts += attempts
                    except (ValueError, AttributeError):
                        pass
                if game.ht_pim is not None:
                    total_pim += game.ht_pim
                total_games += 1

            elif game.awayteam == team_abbrev:
                if game.at_powerplayconversion:
                    try:
                        goals, attempts = map(int, game.at_powerplayconversion.split('/'))
                        total_pp_goals += goals
                        total_pp_attempts += attempts
                    except (ValueError, AttributeError):
                        pass
                if game.at_pim is not None:
                    total_pim += game.at_pim
                total_games += 1

        powerplay_pct = (total_pp_goals / total_pp_attempts * 100) if total_pp_attempts > 0 else 0
        avg_pim_per_game = (total_pim / total_games) if total_games > 0 else 0

        return {
            "total_pp_goals": total_pp_goals,
            "total_pp_attempts": total_pp_attempts,
            "powerplay_pct": round(powerplay_pct, 2),
            "total_pim": total_pim,
            "avg_pim_per_game": round(avg_pim_per_game, 2),
            "total_games": total_games
        }

async def get_team_hits_blocks_stats(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        total_hits = 0
        total_blocks = 0
        total_games = 0

        for game, in games:
            if game.hometeam == team_abbrev:
                if game.ht_hits is not None:
                    total_hits += game.ht_hits
                if game.ht_blocks is not None:
                    total_blocks += game.ht_blocks
                total_games += 1

            elif game.awayteam == team_abbrev:
                if game.at_hits is not None:
                    total_hits += game.at_hits
                if game.at_blocks is not None:
                    total_blocks += game.at_blocks
                total_games += 1

        avg_hits = (total_hits / total_games) if total_games > 0 else 0
        avg_blocks = (total_blocks / total_games) if total_games > 0 else 0

        return {
            "total_hits": total_hits,
            "total_blocks": total_blocks,
            "avg_hits": round(avg_hits, 2),
            "avg_blocks": round(avg_blocks, 2),
            "total_games": total_games
        }
async def get_team_streaks(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            ).order_by(Games.gamedate)
        )
        games = result.fetchall()

        win_streak = 0
        loss_streak = 0
        max_win_streak = 0
        max_loss_streak = 0

        for game, in games:
            is_win = (
                (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
                (game.awayteam == team_abbrev and game.at_score > game.ht_score)
            )
            is_loss = (
                (game.hometeam == team_abbrev and game.ht_score < game.at_score) or
                (game.awayteam == team_abbrev and game.at_score < game.ht_score)
            )
            is_draw = game.period_number > 3  # ничья в основное время

            if is_win:
                win_streak += 1
                loss_streak = 0
                if win_streak > max_win_streak:
                    max_win_streak = win_streak
            elif is_loss:
                loss_streak += 1
                win_streak = 0
                if loss_streak > max_loss_streak:
                    max_loss_streak = loss_streak
            else:
                # ничья — обнуляем обе серии
                win_streak = 0
                loss_streak = 0

        return {
            "max_win_streak": max_win_streak,
            "max_loss_streak": max_loss_streak
        }

async def get_team_home_away_stats(team_abbrev: str):
    async with async_session() as session:
        result = await session.execute(
            select(Games).where(
                or_(Games.hometeam == team_abbrev, Games.awayteam == team_abbrev)
            )
        )
        games = result.fetchall()

        home_wins = 0
        home_losses = 0
        away_wins = 0
        away_losses = 0

        for game, in games:
            if game.hometeam == team_abbrev:
                if game.ht_score > game.at_score:
                    home_wins += 1
                else:
                    home_losses += 1
            elif game.awayteam == team_abbrev:
                if game.at_score > game.ht_score:
                    away_wins += 1
                else:
                    away_losses += 1

        return {
            "home_wins": home_wins,
            "home_losses": home_losses,
            "away_wins": away_wins,
            "away_losses": away_losses
        }