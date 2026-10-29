import random

from Models import StrategyGenome


class Crossover:
    @staticmethod
    def create_child(
        parent1: StrategyGenome,
        parent2: StrategyGenome,
    ) -> StrategyGenome:

        if parent1.fast_ema >= parent1.slow_ema:
            raise ValueError("Parent 1 has an invalid genome.")

        if parent2.fast_ema >= parent2.slow_ema:
            raise ValueError("Parent 2 has an invalid genome.")

        candidates = [
            StrategyGenome(
                fast_ema=parent1.fast_ema,
                slow_ema=parent2.slow_ema,
            ),
            StrategyGenome(
                fast_ema=parent2.fast_ema,
                slow_ema=parent1.slow_ema,
            ),
        ]

        valid_candidates = [
            child
            for child in candidates
            if child.fast_ema < child.slow_ema
        ]

        return random.choice(valid_candidates)