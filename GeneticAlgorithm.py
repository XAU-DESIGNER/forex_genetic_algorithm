from Models import StrategyGenome, Strategy
from TournamentSelection import TournamentSelection
from Crossover import Crossover
from Mutation import Mutation
from FitnessEvaluator import FitnessEvaluator


class GeneticAlgorithm:

    @staticmethod
    def create_offspring(
        population: list[StrategyGenome],
        fitness_scores: dict[StrategyGenome, float],
        mutation_rate: float = 0.1,
        tournament_size: int = 2,
    ) -> StrategyGenome:

        parent1 = TournamentSelection.select_parent(
            population=population,
            fitness_scores=fitness_scores,
            tournament_size=tournament_size,
        )

        parent2 = TournamentSelection.select_parent(
            population=population,
            fitness_scores=fitness_scores,
            tournament_size=tournament_size,
        )

        child = Crossover.create_child(parent1, parent2)

        return Mutation.mutate(
            genome=child,
            mutation_rate=mutation_rate,
        )

    @staticmethod
    def create_next_generation(
        population: list[StrategyGenome],
        fitness_scores: dict[StrategyGenome, float],
        dataset: dict[StrategyGenome, Strategy],
        evaluator: FitnessEvaluator,
        population_size: int,
        mutation_rate: float = 0.1,
        tournament_size: int = 2,
        max_attempts: int = 5000,
    ) -> tuple[list[StrategyGenome], int]:


        if not population:
            raise ValueError("Population cannot be empty.")

        missing_fitness = [
            genome
            for genome in population
            if genome not in fitness_scores
        ]

        if missing_fitness:
            raise ValueError(
                f"Missing fitness scores for {len(missing_fitness)} genomes."
            )

        invalid_fitness = [
            genome
            for genome in population
            if fitness_scores[genome] is None
        ]

        if invalid_fitness:
            raise ValueError(
                f"Missing valid fitness values for {len(invalid_fitness)} genomes."
            )

        if population_size > len(dataset):
            raise ValueError("Population size cannot exceed dataset size.")

        if population_size <= 0:
            raise ValueError("Population size must be greater than zero.")

        if max_attempts <= 0:
            raise ValueError("Max attempts must be greater than zero.")

        next_generation = []
        seen_genomes = set()
        attempts = 0

        while len(next_generation) < population_size and attempts < max_attempts:
            attempts += 1

            child = GeneticAlgorithm.create_offspring(
                population=population,
                fitness_scores=fitness_scores,
                mutation_rate=mutation_rate,
                tournament_size=tournament_size,
            )

            # Never allow an invalid genome into the next generation.
            if child.fast_ema >= child.slow_ema:
                continue

            if child in seen_genomes:
                continue

            strategy = dataset.get(child)

            if strategy is None:
                continue

            fitness = evaluator.calculate_fitness(strategy)

            if fitness is None:
                continue

            seen_genomes.add(child)
            next_generation.append(child)

        return next_generation, attempts