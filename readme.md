# Forex genetic algorithm (strategy optimization)
# Genetic Algorithm

An educational project demonstrating Genetic Algorithms for trading strategy optimization using Python and .NET.

## Requirements

- .NET 10 SDK
- Python 3
- Python `requests` package

## How to Run

**Step 1: Start the .NET Backtester**

Make sure .NET 10 SDK is installed.

Open a terminal in the project root and run:

```bash
dotnet run --project SimulatedBacktester/SimulatedBacktester.csproj --urls http://localhost:5186
```

Keep this terminal running.

**Step 2: Run the Python Application**

After the .NET Backtester has started successfully, open another terminal and run:

```bash
pip install requests
python3 GeneticAlgorithm/Main.py
```

The Python application communicates with the .NET Backtester API to evaluate genomes.

**Important:** Always start the .NET project before running the Python application.