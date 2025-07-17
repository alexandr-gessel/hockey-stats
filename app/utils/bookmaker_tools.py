# utils/bookmaker_tools.py

def corrected_probability_3way(quote_team: float, quote_draw: float, quote_opponent: float) -> float:
    """
    Корректировка на маржу букмекера для трёх исходов:
    Победа команды, ничья, победа соперника.
    Возвращает корректированную вероятность победы команды.
    """
    if quote_team <= 0 or quote_draw <= 0 or quote_opponent <= 0:
        return 0  # страховка от нулевых или отрицательных котировок
    
    market_sum = (1 / quote_team) + (1 / quote_draw) + (1 / quote_opponent)
    return (1 / quote_team) / market_sum