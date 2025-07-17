# repositories/team_upset_repository.py

from sqlalchemy import select, or_, and_
from collections import defaultdict
from app.db import async_session
from app.models import Games, Quotes
from app.crud import get_team_by_abbrev, get_games_with_quotes_for_team
from app.utils.upset_rules import is_upset_relative
from datetime import timedelta

GAMETYPE_STAGE_MAP = {1: "preseason", 2: "regular", 3: "playoff"}

def get_opponent_abbrev(game, team_abbrev):
    return game.awayteam if game.hometeam == team_abbrev else game.hometeam

def validate_quote_pair(quote, team_name, opponent_name):
    return (
        (quote.name_1 == team_name and quote.name_2 == opponent_name) or
        (quote.name_2 == team_name and quote.name_1 == opponent_name)
    )

def get_quotes_for_team_and_opponent(quote, team_name):
    return (quote.quote_1, quote.quote_2) if quote.name_1 == team_name else (quote.quote_2, quote.quote_1)

def is_team_winner(game, team_abbrev):
    return (
        (game.hometeam == team_abbrev and game.ht_score > game.at_score) or
        (game.awayteam == team_abbrev and game.at_score > game.ht_score)
    )

async def get_team_upsets(team_abbrev, threshold_diff=0.25):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return []

        rows = await get_games_with_quotes_for_team(session, team.name, team_abbrev)
        upsets = []

        for game, quote in rows:
            opponent = await get_team_by_abbrev(session, get_opponent_abbrev(game, team_abbrev))
            if not opponent or not validate_quote_pair(quote, team.name, opponent.name):
                continue

            tq, oq = get_quotes_for_team_and_opponent(quote, team.name)
            if is_upset_relative(tq, oq, threshold_diff) and is_team_winner(game, team_abbrev):
                upsets.append((game, quote))

        return upsets

async def get_team_upsets_by_stage(team_abbrev, percent_diff=0.25):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return {}

        rows = await get_games_with_quotes_for_team(session, team.name, team_abbrev)
        stage_upsets = defaultdict(int)
        stage_totals = defaultdict(int)

        for game, quote in rows:
            opponent = await get_team_by_abbrev(session, get_opponent_abbrev(game, team_abbrev))
            if not opponent or not validate_quote_pair(quote, team.name, opponent.name):
                continue

            tq, oq = get_quotes_for_team_and_opponent(quote, team.name)
            stage = GAMETYPE_STAGE_MAP.get(game.gametype, "unknown")
            stage_totals[stage] += 1

            if is_upset_relative(tq, oq, percent_diff) and is_team_winner(game, team_abbrev):
                stage_upsets[stage] += 1

        return {
            "stages": list(stage_totals.keys()),
            "totals": dict(stage_totals),
            "upsets": dict(stage_upsets)
        }

async def get_avg_upset_quote_for_team(team_abbrev, percent_diff=0.25):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return 0

        rows = await get_games_with_quotes_for_team(session, team.name, team_abbrev)
        quotes = []

        for game, quote in rows:
            opponent = await get_team_by_abbrev(session, get_opponent_abbrev(game, team_abbrev))
            if not opponent or not validate_quote_pair(quote, team.name, opponent.name):
                continue

            tq, oq = get_quotes_for_team_and_opponent(quote, team.name)
            if is_upset_relative(tq, oq, percent_diff) and is_team_winner(game, team_abbrev):
                quotes.append(tq)

        return round(sum(quotes) / len(quotes), 2) if quotes else 0

async def get_team_upsets_with_quote_threshold(team_abbrev, quote_threshold=2.50, percent_diff=0.25):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return {"total_games_with_high_quote": 0, "upsets_with_high_quote": 0}

        rows = await get_games_with_quotes_for_team(session, team.name, team_abbrev)
        total, upsets = 0, 0

        for game, quote in rows:
            opponent = await get_team_by_abbrev(session, get_opponent_abbrev(game, team_abbrev))
            if not opponent or not validate_quote_pair(quote, team.name, opponent.name):
                continue

            tq, oq = get_quotes_for_team_and_opponent(quote, team.name)
            if tq > quote_threshold:
                total += 1
                if is_upset_relative(tq, oq, percent_diff) and is_team_winner(game, team_abbrev):
                    upsets += 1

        return {"total_games_with_high_quote": total, "upsets_with_high_quote": upsets}

async def get_home_losses_as_favorite(team_abbrev):
    async with async_session() as session:
        team = await get_team_by_abbrev(session, team_abbrev)
        if not team:
            print(f"Team {team_abbrev} nicht gefunden.")
            return {"total_home_games": 0, "home_fav_losses": 0}

        rows = await get_games_with_quotes_for_team(session, team.name, team_abbrev)
        total, losses = 0, 0

        for game, quote in rows:
            if game.hometeam != team_abbrev:
                continue

            opponent = await get_team_by_abbrev(session, game.awayteam)
            if not opponent or not validate_quote_pair(quote, team.name, opponent.name):
                continue

            tq, oq = get_quotes_for_team_and_opponent(quote, team.name)
            total += 1

            if tq < oq and game.ht_score < game.at_score:
                losses += 1

        return {"total_home_games": total, "home_fav_losses": losses}
