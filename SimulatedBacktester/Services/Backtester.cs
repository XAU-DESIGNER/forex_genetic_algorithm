using SimulatedBacktester.Contracts;

namespace SimulatedBacktester.Services;

public class Backtester
{
    private const double OptimalFastEma = 10;
    private const double OptimalSlowEma = 30;

    public BacktestResult Start(BacktestRequest request)
    {
        if (request.InitialBalance <= 0)
            throw new ArgumentException("Initial balance must be positive.");

        if (request.FastEma <= 0 || request.SlowEma <= 0)
            throw new ArgumentException("EMA values must be positive.");

        if (request.FastEma >= request.SlowEma)
            throw new ArgumentException("Fast EMA must be smaller than Slow EMA.");

        var quality = CalculateStrategyQuality(request);

        var result = new BacktestResult
        {
            InitialBalance = request.InitialBalance,

            OutCome = GenerateOutcome(quality),

            TotalCommission = GenerateCommission(request),

            Swap = GenerateSwap(),

            Drawdown = GenerateDrawdown(quality),

            ProfitFactor = GenerateProfitFactor(quality)
        };

        return result;
    }

    private static double CalculateStrategyQuality(BacktestRequest request)
    {
        var fastDistance = (double)request.FastEma - OptimalFastEma;
        var slowDistance = ((double)request.SlowEma - OptimalSlowEma) / 2;

        var distance = Math.Pow(fastDistance / 8, 2)
                     + Math.Pow(slowDistance / 8, 2);

        return Math.Exp(-0.5 * distance);
    }

    private static decimal GenerateOutcome(double quality)
    {
        var expectedOutcome = -30 + (180 * quality);

        return (decimal)(expectedOutcome + RandomNoise(-60, 60));
    }

    private static decimal GenerateCommission(BacktestRequest request)
    {
        var tradeIntensity = Math.Clamp(
            1 + (double)request.FastEma / 20,
            0.5,
            2.5
        );

        var commission = RandomNoise(4, 14) * tradeIntensity;

        return (decimal)commission;
    }

    private static decimal GenerateSwap()
    {
        // 10% probability of swap
        if (Random.Shared.NextDouble() > 0.1)
            return 0;

        return (decimal)RandomNoise(-10, 3);
    }

    private static decimal GenerateDrawdown(double quality)
    {
        var expectedDrawdown = 14 - (8 * quality);

        var drawdown = expectedDrawdown + RandomNoise(-4, 4);

        return (decimal)Math.Clamp(drawdown, 1, 30);
    }

    private static decimal GenerateProfitFactor(double quality)
    {
        var expectedProfitFactor = 0.75 + (1.4 * quality);

        var profitFactor = expectedProfitFactor + RandomNoise(-0.45, 0.45);

        return (decimal)Math.Clamp(profitFactor, 0.3, 4);
    }

    private static double RandomNoise(double min, double max)
    {
        return min + Random.Shared.NextDouble() * (max - min);
    }
}