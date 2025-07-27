# app/repositories/games.py

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def load_all_games():
    path = Path("app/static/data/games.json")
    return json.loads(path.read_text())

def get_games(limit=20, offset=0):
    all_games = load_all_games()
    return all_games[offset : offset + limit]

def get_games_grouped_by_date_with_cutoff(limit=20, offset=0, search_team="", search_date="", check_next_page=True):
    games = load_all_games()  # Чтение всех игр сразу

    
    filtered = []
    for game in games:
        if search_team:
            if search_team.lower() not in game["home_team"].lower() and search_team.lower() not in game["away_team"].lower():
                continue
        if search_date:
            if datetime.strptime(game["date"], "%Y-%m-%d").strftime("%Y-%m-%d") != search_date:
                continue
        filtered.append(game)

    
    grouped = defaultdict(list)
    for game in filtered:
        grouped[game["date"]].append(game)

    grouped_sorted = sorted(grouped.items(), key=lambda x: x[0], reverse=True)

    
    result = []
    total = 0
    i = offset 
    while i < len(grouped_sorted) and total < limit:
        date, games_on_date = grouped_sorted[i]
        result.append((date, games_on_date))
        total += len(games_on_date)
        i += 1

    
    has_next_page = False
    if check_next_page:
        while i < len(grouped_sorted):
            if grouped_sorted[i][1]:
                has_next_page = True
                break
            i += 1

    return result, has_next_page