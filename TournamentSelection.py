import random

from Models import StrategyGenome


class TournamentSelection:
    @staticmethod
    def select_parent(
        population: list[StrategyGenome],
        fitness_scores: dict[StrategyGenome, float],
        tournament_size: int = 2,
    ) -> StrategyGenome:

        if not population:
            raise ValueError("Population cannot be empty.")

        if tournament_size <= 0:
            raise ValueError("Tournament size must be greater than zero.")

        if any(genome not in fitness_scores for genome in population):
            raise ValueError("Every genome must have a fitness score.")

        candidates = random.sample(
            population,
            k=min(tournament_size, len(population)),
        )

        return max(candidates, key=lambda genome: fitness_scores[genome])