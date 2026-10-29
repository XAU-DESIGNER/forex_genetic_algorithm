import random

from Models import StrategyGenome


class Mutation:
    @staticmethod
    def mutate(
        genome: StrategyGenome,
        mutation_rate: float = 0.1,
        max_change: int = 5,
        min_ema: int = 2,
        max_ema: int = 200,
    ) -> StrategyGenome:

        if not 0 <= mutation_rate <= 1:
            raise ValueError("Mutation rate must be between 0 and 1.")

        if max_change < 1:
            raise ValueError("Max change must be at least 1.")

        if min_ema > max_ema:
            raise ValueError("min_ema cannot exceed max_ema.")

        # Reject an invalid input genome instead of returning it silently.
        if genome.fast_ema >= genome.slow_ema:
            raise ValueError("Genome must satisfy fast_ema < slow_ema.")

        fast_ema = genome.fast_ema
        slow_ema = genome.slow_ema

        if random.random() < mutation_rate:
            fast_ema += random.choice([-1, 1]) * random.randint(1, max_change)

        if random.random() < mutation_rate:
            slow_ema += random.choice([-1, 1]) * random.randint(1, max_change)

        fast_ema = max(min_ema, min(fast_ema, max_ema))
        slow_ema = max(min_ema, min(slow_ema, max_ema))

        # Cancel an invalid mutation; the original genome is valid.
        if fast_ema >= slow_ema:
            return genome

        return StrategyGenome(
            fast_ema=fast_ema,
            slow_ema=slow_ema,
        )