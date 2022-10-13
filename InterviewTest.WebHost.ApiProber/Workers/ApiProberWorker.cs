using System.Timers;
using InterviewTest.WebHost.ApiProber.Interfaces;

namespace InterviewTest.WebHost.ApiProber.Workers;

public class ApiProberWorker : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<ApiProberWorker> _logger;

    public ApiProberWorker(IServiceProvider serviceProvider, ILogger<ApiProberWorker> logger)
    {
        _serviceProvider = serviceProvider;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken token)
    {
        const int rpm = 5;
        const int millisecondsInMinute = 60 * 1000;
        const int delayTimeMilliseconds = millisecondsInMinute / rpm;
        var standardDelay = TimeSpan.FromMilliseconds(delayTimeMilliseconds);
        while (!token.IsCancellationRequested)
        {
            var startTime = DateTime.Now;
            FireApiProbe();
            var executionTime = DateTime.Now - startTime;
            var currentDelay = standardDelay - executionTime;
            Console.WriteLine(currentDelay);
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