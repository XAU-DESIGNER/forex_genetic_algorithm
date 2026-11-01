namespace SimulatedBacktester.Contracts;

public class BacktestRequest
{
    public decimal InitialBalance { get; set; } = 1000;
    public decimal SlowEma { get; set; } = 20;
    public decimal FastEma { get; set; } = 10;
}