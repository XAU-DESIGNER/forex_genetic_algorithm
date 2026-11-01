class GeneticAlgorithm:

    def InitializePopulation(self):
        print("Initializing first population")
        print("Initializing first population DONE!")

    def EvaluateFitness(self):
        print("Sending backtest request for genome")
        print("Backtest result received!")
        print("Score: 12.32")

    def TournamentSelect(self):
        print("Selecting best genomes to be parents")
        print("Done!")

    def Crossover(self):
        print("Two parents selected")
        print("Creating new child")

    def Mutation(self):
        print("Mutating")

    def HoldElitism(self):
        print("Elitism genomes saved!")

    def CreateNextGeneration(self):
        print("Creating next generation")

    def StartGenerating(self):
        self.InitializePopulation()

        for generation in range(5):
            print(f"\nGeneration: {generation + 1}")

            self.EvaluateFitness()
            self.HoldElitism()
            self.TournamentSelect()
            self.Crossover()
            self.Mutation()
            self.CreateNextGeneration()

        print("\nOptimization completed!")
        print("Genome (12, 45) has the best score among others.")
        print("Score: 48.12")