# utils/upset_rules.py

def is_upset(quote_team: float, quote_opponent: float, threshold_diff: float = 0.25) -> bool:
    """
    Gibt True zurück, wenn das Team ein Außenseiter im Paar ist (der Koeffizient ist um einen bestimmten Schwellenwert höher)
    threshold_diff — Mindestdifferenz zwischen den Koeffizienten (0,25 = 25%)
    """
    return (quote_team - quote_opponent) >= threshold_diff


def is_upset_relative(quote_team: float, quote_opponent: float, percent_diff: float = 0.25) -> bool:
    """
    Apset, wenn die Quote des Teams um percent_diff Prozent höher ist als die des Gegners
    """
    if quote_opponent == 0:
        return False
    return (quote_team - quote_opponent) / quote_opponent >= percent_diff


def is_upset_delta_threshold(quote_team: float, quote_opponent: float, delta: float = 0.4, min_quote: float = 2.2) -> bool:
    """
    Apset, wenn das Delta zwischen den Kursen größer ist als der Schwellenwert und der Teamkoeffizient nicht kleiner ist als min_quote
    """
    return (quote_team - quote_opponent) >= delta and quote_team >= min_quote

