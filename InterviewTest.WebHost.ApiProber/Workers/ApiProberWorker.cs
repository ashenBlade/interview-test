using System.Timers;
using InterviewTest.WebHost.ApiProber.Interfaces;

namespace InterviewTest.WebHost.ApiProber.Workers;

public class ApiProberWorker : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<ApiProberWorker> _logger;
    private readonly int _rpm;

    private const double SecondsInMinute = 60;
    private TimeSpan RpmDelay => TimeSpan.FromMilliseconds(SecondsInMinute / _rpm);

    public ApiProberWorker(IServiceProvider serviceProvider, ILogger<ApiProberWorker> logger, int rpm)
    {
        if (rpm < 1)
        {
            throw new ArgumentOutOfRangeException(nameof(rpm), rpm, "RPM must be positive");
        }
        
        _serviceProvider = serviceProvider;
        _logger = logger;
        _rpm = rpm;
    }

    protected override async Task ExecuteAsync(CancellationToken token)
    {
        var betweenFireDelay = RpmDelay;
        while (!token.IsCancellationRequested)
        {
            var startTime = DateTime.Now;
            _logger.LogTrace("Start probing at: {StartTime}", startTime);
            FireApiProbe();
            var executionTime = DateTime.Now - startTime;
            _logger.LogTrace("Execution time: {ExecutionTime}", executionTime);
            var currentDelay = betweenFireDelay - executionTime;
            _logger.LogTrace("Sleeping for: {Delay}", currentDelay);
            await Task.Delay(currentDelay.Milliseconds, token);
        }
        void FireApiProbe()
        {
            Task.Run(async () =>
            {
                await using var scope = _serviceProvider.CreateAsyncScope();
                var prober = scope.ServiceProvider.GetRequiredService<IApiProber>();
                try
                {
                    var result = await prober.ProbeAsync(token);
                    if (result.Succeed)
                    {
                        _logger.LogError("API probe succeed at");
                    }
                    else
                    {
                        _logger.LogWarning(result.Exception, 
                                           "Could not probe API. Error description: {ErrorMessage}",
                                           result.ErrorMessage!);
                    }
                }
                catch (Exception unhandled)
                {
                    _logger.LogError(unhandled, "Unhandled exception occured while probing API");
                }
            }, token);
        }
    }
}