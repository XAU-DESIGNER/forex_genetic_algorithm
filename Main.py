from DataLoader import DataLoader
from PopulationInitializer import PopulationInitializer
from FitnessEvaluator import FitnessEvaluator
from GeneticAlgorithm import GeneticAlgorithm


# Configuration
POPULATION_SIZE = 20
GENERATIONS = 10
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 2
MAX_ATTEMPTS = 5000


# Load dataset
print("Loading data...")

dataset = DataLoader.load_data()

print("Data loaded successfully")
print(f"Total strategies in dataset: {len(dataset)}")


# Initialize evaluator
evaluator = FitnessEvaluator(
    max_drawdown=5.0,
    max_losing_streak=8,
)


# Initialize population using valid strategies only
population = PopulationInitializer.initialize(
    dataset=dataset,
    evaluator=evaluator,
    population_size=POPULATION_SIZE,
)

fitness_scores = {
    genome: evaluator.calculate_fitness(dataset[genome])
    for genome in population
}

print(f"Initial population size: {len(population)}")


# Track the best strategy found across all generations
best_genome = max(
    population,
    key=lambda genome: fitness_scores[genome],
)

best_fitness = fitness_scores[best_genome]

print(f"\nInitial best fitness: {best_fitness:.4f}")
print(f"Initial best strategy: {best_genome}")


# Run genetic algorithm
for generation in range(1, GENERATIONS + 1):

    next_generation, attempts = GeneticAlgorithm.create_next_generation(
        population=population,
        fitness_scores=fitness_scores,
        dataset=dataset,
        evaluator=evaluator,
        population_size=POPULATION_SIZE,
        mutation_rate=MUTATION_RATE,
        tournament_size=TOURNAMENT_SIZE,
        max_attempts=MAX_ATTEMPTS,
    )

    if len(next_generation) < POPULATION_SIZE:
        print(
            f"\nGeneration {generation} stopped: "
            f"only {len(next_generation)} unique valid offspring "
            f"found after {attempts} attempts."
        )
        break

    population = next_generation

    fitness_scores = {
        genome: evaluator.calculate_fitness(dataset[genome])
        for genome in population
    }

    generation_best = max(
        population,
        key=lambda genome: fitness_scores[genome],
    )

    generation_best_fitness = fitness_scores[generation_best]

    if generation_best_fitness > best_fitness:
        best_genome = generation_best
        best_fitness = generation_best_fitness

    print(
        f"Generation {generation:02} | "
        f"Best Fitness: {generation_best_fitness:.4f} | "
        f"Attempts: {attempts}"
    )


# Final result
best_strategy = dataset[best_genome]

print("\n========== FINAL RESULT ==========")
print(f"Best genome: {best_genome}")
print(f"Fitness: {best_fitness:.4f}")
print(f"Fast EMA: {best_genome.fast_ema}")
print(f"Slow EMA: {best_genome.slow_ema}")
print(f"PnL: {best_strategy.pnl}")
print(f"Drawdown: {best_strategy.drawdown}")
print(f"Losing streak: {best_strategy.losing_streak}")
print("==================================")