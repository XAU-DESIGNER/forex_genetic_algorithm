from dataclasses import dataclass


@dataclass
class Strategy:
    fast_ema: int
    slow_ema: int
    losing_streak: int
    drawdown: float
    pnl: float
    average_spread: float
    initial_balance: float


@dataclass
class StrategyGenome:
    fast_ema: int
    slow_ema: int
