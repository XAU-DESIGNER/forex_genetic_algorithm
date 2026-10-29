import csv

from Models import Strategy, StrategyGenome

class DataLoader:
    @staticmethod
    def load_data() -> dict[StrategyGenome, Strategy]:
        strategies = {}
        print("Loading data")
        with open(
            f"data/strategies.csv",
            encoding="utf-8",
            newline=""
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                strategy = Strategy(
                    fast_ema=int(row["fast_ema"]),
                    slow_ema=int(row["slow_ema"]),
                    losing_streak=int(row["losing_streak"]),
                    drawdown=float(row["drawdown"]),
                    pnl=float(row["PnL"]),
                    average_spread=float(row["avg_spread"]),
                    initial_balance=float(row["initial_balance"]),
                )

                genome = StrategyGenome(
                    fast_ema=strategy.fast_ema,
                    slow_ema=strategy.slow_ema,
                )

                if genome in strategies:
                    print(genome)
                    raise ValueError(
                        f"Duplicate genome found: {genome}"
                    )

                strategies[genome] = strategy
        print("Data loaded successfuly")
        return strategies