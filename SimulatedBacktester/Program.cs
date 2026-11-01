using Scalar.AspNetCore;
using SimulatedBacktester.Contracts;
using SimulatedBacktester.Services;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapOpenApi();
app.MapScalarApiReference();
builder.Services.AddSingleton<Backtester>();

app.MapGet("/", () => "backtest service is ready (simulated and nothing is real)");

app.MapGet("/start", (decimal fastEma, decimal slowEma, decimal initialBalance, Backtester backtester) =>
{
    var request = new BacktestRequest
    {
        FastEma = fastEma,
        SlowEma = slowEma,
        InitialBalance = initialBalance
    };

    var result = backtester.Start(request);

    return Results.Ok(result);
});

app.Run();