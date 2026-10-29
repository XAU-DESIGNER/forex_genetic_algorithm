import random

from Models import StrategyGenome, Strategy
from FitnessEvaluator import FitnessEvaluator


class PopulationInitializer:
    @staticmethod
    def initialize(
        dataset: dict[StrategyGenome, Strategy],
        evaluator: FitnessEvaluator,
        population_size: int,
    ) -> list[StrategyGenome]:

        if population_size <= 0:
            raise ValueError("Population size must be greater than zero.")

        valid_genomes = []

        for genome, strategy in dataset.items():
            fitness = evaluator.calculate_fitness(strategy)

            if fitness is not None:
                valid_genomes.append(genome)

        if population_size > len(valid_genomes):
            raise ValueError(
                f"Population size ({population_size}) exceeds "
                f"the number of valid genomes ({len(valid_genomes)})."
            )

        return random.sample(valid_genomes, k=population_size)