from Models import StrategyGenome, Strategy

class FitnessEvaluator:
    def __init__(self , max_drawdown: float = 5.0, max_losing_streak: int = 8):
        self.max_drawdown = max_drawdown
        self.max_losing_streak = max_losing_streak

    def calculate_fitness(self, strategy: Strategy) -> float | None:
        if strategy.drawdown > self.max_drawdown:
            return None

        if strategy.losing_streak > self.max_losing_streak:
            return None

        if strategy.initial_balance <= 0:
            return None

        if strategy.drawdown <= 0:
            return None

        roi = (strategy.pnl / strategy.initial_balance) * 100
        fitness_score = roi / strategy.drawdown

        return fitness_score