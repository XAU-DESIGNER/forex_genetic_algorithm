namespace SimulatedBacktester.Contracts;

public class BacktestResult
{
    public decimal TotalCommission { get; set; } = 0;
    public decimal OutCome { get; set; } = 0;
    public decimal InitialBalance { get; set; }
    public decimal Drawdown { get; set; } = 0;
    public decimal ProfitFactor { get; set; } = 0;
    public decimal Swap { get; set; } = 0;
}