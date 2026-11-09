from Models import StrategyGenome
import random
import requests
import copy


class GeneticAlgorithm:

    def InitializePopulation(self) -> list[StrategyGenome]:
        print("Initializing first population")

        population = []
        population_size = 20

        for _ in range(population_size):
            fast_ema = random.randint(5, 50)
            slow_ema = random.randint(20, 200)

            while fast_ema >= slow_ema:
                slow_ema = random.randint(20, 200)

            genome = StrategyGenome(fast_ema, slow_ema)
            population.append(genome)

        print("Initializing first population DONE!")
        return population

    def EvaluateFitness(self, population: list[StrategyGenome]) -> list[StrategyGenome]:
        print("Evaluating population...")

        for genome in population:
            print(f"Backtesting Genome ({genome.fast_ema}, {genome.slow_ema})")
            response = requests.get(
                "http://localhost:5186/start",
                params={
                    "fastEma": genome.fast_ema,
                    "slowEma": genome.slow_ema,
                    "initialBalance": 1000,
                },
                timeout=30,
            )

            response.raise_for_status()
            result = response.json()

            outcome = result.get("outCome", result.get("outCome", 0))
            swap = result["swap"]
            commission = result["totalCommission"]
            initial_balance = result["initialBalance"]
            drawdown = result["drawdown"]

            roi = ((outcome + swap - commission) / initial_balance) * 100

            if genome.fast_ema < genome.slow_ema and drawdown > 0:
                genome.fitness = roi / drawdown
            else:
                genome.fitness = 0
            print(f"ROI: {roi:.2f}%")
            print(f"Fitness: {genome.fitness:.2f}")

        print("Population evaluation completed!")
        return population

    def TournamentSelect(
        self, population: list[StrategyGenome]
    ) -> list[StrategyGenome]:
        print("Selecting best genomes to be parents")

        parents = []
        parent_count = 4
        tournament_size = 3

        for _ in range(parent_count):
            contestants = random.sample(population, tournament_size)

            winner = max(contestants, key=lambda genome: genome.fitness)

            parents.append(winner)

        print("Parent selection completed!")

        return parents

    def Crossover(self, parents: list[StrategyGenome]) -> list[StrategyGenome]:
        print("Creating offspring")

        offspring = []

        for i in range(0, len(parents), 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]

            child = StrategyGenome(fast_ema=parent1.fast_ema, slow_ema=parent2.slow_ema)

            offspring.append(child)

        print(f"Created {len(offspring)} offspring")

        return offspring

    def Mutation(self, offspring: list[StrategyGenome]) -> list[StrategyGenome]:
        print("Mutating offspring")

        mutation_rate = 0.1

        for genome in offspring:

            if random.random() < mutation_rate:
                genome.fast_ema = random.randint(5, 50)

            if random.random() < mutation_rate:
                genome.slow_ema = random.randint(20, 200)

            if genome.fast_ema >= genome.slow_ema:
                genome.slow_ema = random.randint(genome.fast_ema + 1, 200)

        print("Mutation completed!")

        return offspring

    def HoldElitism(self, population: list[StrategyGenome]) -> list[StrategyGenome]:
        elite_count = 2

        elites = copy.deepcopy(
            sorted(population, key=lambda genome: genome.fitness, reverse=True)[
                :elite_count
            ]
        )

        print(f"Preserved {len(elites)} elite genomes")

        return elites

    def CreateNextGeneration(
        self,
        elites: list[StrategyGenome],
        offspring: list[StrategyGenome],
        population_size: int,
    ) -> list[StrategyGenome]:

        print("Creating next generation")

        next_generation = []

        next_generation.extend(elites)
        next_generation.extend(offspring)

        while len(next_generation) < population_size:
            fast_ema = random.randint(5, 50)
            slow_ema = random.randint(fast_ema + 1, 200)

            genome = StrategyGenome(fast_ema, slow_ema)
            next_generation.append(genome)

        print(f"Next generation created: {len(next_generation)} genomes")

        return next_generation

    def StartGenerating(self):

        population_size = 20
        population = self.InitializePopulation()

        best_genome = None

        for generation in range(300):
            print(f"\nGeneration: {generation + 1}")

            population = self.EvaluateFitness(population)

            elites = self.HoldElitism(population)

            generation_best = max(population, key=lambda genome: genome.fitness)

            if best_genome is None or generation_best.fitness > best_genome.fitness:
                best_genome = copy.deepcopy(generation_best)

            parents = self.TournamentSelect(population)

            children = self.Crossover(parents)

            children = self.Mutation(children)

            population = self.CreateNextGeneration(elites, children, population_size)

        print("\nOptimization completed!")

        print(f"Best Genome: ({best_genome.fast_ema}, {best_genome.slow_ema})")
        print(f"Best Fitness: {best_genome.fitness:.2f}")

        return best_genome
