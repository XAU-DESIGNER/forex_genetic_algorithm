# Forex genetic algorithm (strategy optimization)

problem: find best parameters
goal: repeat 5 times, return strategy with best score
other:
$$Genome=[fast\_ema,slow\_ema] \\[20pt] ROI=\frac{Outcome+Swap-Commission}{InitialBalance}\times100 \\[20pt] Fitness(Genome)= \begin{cases} \dfrac{ROI}{Drawdown} & fast<slow \land Drawdown>0\\[10pt] 0 & otherwise \end{cases} \\[15pt] Goal=\max_{Genome} Fitness(Genome)$$
## Phase 1: .NET API
a c# web project that has
```
http get /start
```

returns randomlly:
```json
{
	"Total_commission":1.2,
	"Outcome":210.00,
	"Initial_balance":1000.00,
	"DrawDown":8.1,
	"Profit_factor":1.5,
	"Swap":-12.00
}
```

## Phase 2: Genetic Algorithm
>For this example, I used Python as the primary programming language.
### Algorithm

1. **Initialize Population**
    
    - Generate a random population of genomes.
        
    - Each genome contains two genes: `fast_ema` and `slow_ema`.
        
    - Ensure that `fast_ema < slow_ema`.
        
2. **Evaluate Fitness**
    
    - For each genome:
        
        - Send a GET request to the .NET API (`/start`).
            
        - Receive the backtest results.
            
        - Calculate ROI using the returned metrics.
            
        - Calculate the fitness score.
            
        - Assign a fitness score of `0` if the genome is invalid.
            
3. **Selection**
    
    - Select the fittest genomes from the current population.
        
    - Use them as parents for the next generation.
        
4. **Crossover**
    
    - Select two parents.
        
    - Combine their genes to create new offspring.
        
    - Ensure that the offspring satisfies the genome constraints.
        
5. **Mutation**
    
    - Randomly modify one or both genes with a predefined mutation probability.
        
    - Ensure that the mutated genome remains valid.
        
6. **Create Next Generation**
    
    - Combine selected parents and offspring to form the next population.
        
    - Preserve the best-performing genome using elitism.
        
7. **Repeat**
    
    - Repeat the evaluation and evolution process for 5 generations.
        
    - Track the best-performing genome across all generations.
        
8. **Return Result**
    
    - Return the genome with the highest fitness score found during the entire process.
        

### Final Output

The algorithm returns the best-performing strategy parameters:

- `fast_ema`
    
- `slow_ema`
    
- `fitness_score`
    
- `ROI`
    
- `Drawdown`