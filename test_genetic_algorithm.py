import unittest
from unittest.mock import patch

from Models import StrategyGenome
from Mutation import Mutation
from GeneticAlgorithm import GeneticAlgorithm
from FitnessEvaluator import FitnessEvaluator


class TestGeneticAlgorithm(unittest.TestCase):

    def test_mutation_rejects_invalid_genome(self):
        invalid_genome = StrategyGenome(
            fast_ema=30,
            slow_ema=20,
        )

        with self.assertRaises(ValueError):
            Mutation.mutate(invalid_genome)

    def test_mutation_never_returns_invalid_genome(self):
        genome = StrategyGenome(
            fast_ema=20,
            slow_ema=21,
        )

        # Repeatedly test mutation, including mutations that could
        # make fast_ema >= slow_ema.
        for _ in range(100):
            child = Mutation.mutate(
                genome=genome,
                mutation_rate=1.0,
                max_change=5,
            )

            self.assertLess(child.fast_ema, child.slow_ema)

    def test_invalid_child_never_enters_next_generation(self):
        parent = StrategyGenome(
            fast_ema=10,
            slow_ema=20,
        )

        invalid_child = StrategyGenome(
            fast_ema=30,
            slow_ema=20,
        )

        dataset = {
            parent: type(
                "FakeStrategy",
                (),
                {
                    "fast_ema": 10,
                    "slow_ema": 20,
                    "drawdown": 1.0,
                    "losing_streak": 1,
                    "initial_balance": 1000.0,
                    "pnl": 100.0,
                    "average_spread": 1.0,
                },
            )()
        }

        evaluator = FitnessEvaluator()

        with patch.object(
            GeneticAlgorithm,
            "create_offspring",
            return_value=invalid_child,
        ):
            next_generation, attempts = (
                GeneticAlgorithm.create_next_generation(
                    population=[parent],
                    fitness_scores={parent: 10.0},
                    dataset=dataset,
                    evaluator=evaluator,
                    population_size=1,
                    max_attempts=3,
                )
            )

        self.assertEqual(next_generation, [])
        self.assertEqual(attempts, 3)

    def test_missing_fitness_stops_parent_selection(self):
        parent1 = StrategyGenome(10, 20)
        parent2 = StrategyGenome(12, 25)

        with patch(
            "GeneticAlgorithm.TournamentSelection.select_parent"
        ) as select_parent:
            with self.assertRaises(ValueError):
                GeneticAlgorithm.create_next_generation(
                    population=[parent1, parent2],
                    fitness_scores={parent1: 10.0},
                    dataset={},
                    evaluator=FitnessEvaluator(),
                    population_size=1,
                )

            select_parent.assert_not_called()


if __name__ == "__main__":
    unittest.main()