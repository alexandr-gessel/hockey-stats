# utils/team_colors.py

TEAM_COLORS = {
    "ANA": "#FC4C02",   # Anaheim Ducks
    "ARI": "#8C2633",   # Arizona Coyotes
    "BOS": "#FFB81C",   # Boston Bruins
    "BUF": "#003087",   # Buffalo Sabres
    "CGY": "#C8102E",   # Calgary Flames
    "CAR": "#CC0000",   # Carolina Hurricanes
    "CHI": "#CF0A2C",   # Chicago Blackhawks
    "COL": "#6F263D",   # Colorado Avalanche
    "CBJ": "#002654",   # Columbus Blue Jackets
    "DAL": "#006847",   # Dallas Stars
    "DET": "#CE1126",   # Detroit Red Wings
    "EDM": "#041E42",   # Edmonton Oilers
    "FLA": "#C8102E",   # Florida Panthers
    "LAK": "#111111",   # Los Angeles Kings
    "MIN": "#154734",   # Minnesota Wild
    "MTL": "#AF1E2D",   # Montreal Canadiens
    "NSH": "#FFB81C",   # Nashville Predators
    "NJD": "#CE1126",   # New Jersey Devils
    "NYI": "#003087",   # New York Islanders
    "NYR": "#0038A8",   # New York Rangers
    "OTT": "#E31837",   # Ottawa Senators
    "PHI": "#F74902",   # Philadelphia Flyers
    "PIT": "#FFB81C",   # Pittsburgh Penguins
    "SJS": "#006D75",   # San Jose Sharks
    "SEA": "#001628",   # Seattle Kraken
    "STL": "#002F87",   # St. Louis Blues
    "TBL": "#002868",   # Tampa Bay Lightning
    "TOR": "#00205B",   # Toronto Maple Leafs
    "VAN": "#00205B",   # Vancouver Canucks
    "VGK": "#B4975A",   # Vegas Golden Knights
    "WSH": "#CF0A2C",   # Washington Capitals
    "WPG": "#041E42",   # Winnipeg Jets
}


def get_team_color(abbrev: str) -> str:
    """Возвращает HEX цвета команды или серый по умолчанию"""
    return TEAM_COLORS.get(abbrev.upper(), "#999999")