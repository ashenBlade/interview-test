using InterviewTest.WebHost.ApiProber.Infrastructure;
using InterviewTest.WebHost.ApiProber.Interfaces;

namespace InterviewTest.WebHost.ApiProber.Workers;

public class ApiProberWorker : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly ILogger<ApiProberWorker> _logger;
    private readonly TimeSpan _betweenRequestsDelay;

    private const double SecondsInMinute = 60;

    public ApiProberWorker(IServiceProvider serviceProvider, 
                           ILogger<ApiProberWorker> logger,
                           ProbeSettings settings)
    {
        var rpm = settings.Rpm;
        if (rpm < 1)
        {
            throw new ArgumentOutOfRangeException(nameof(rpm), rpm, "RPM must be positive");
        }
        
        _betweenRequestsDelay = TimeSpan.FromSeconds(SecondsInMinute / rpm);
        _serviceProvider = serviceProvider;
        _logger = logger;
    }
    
    protected override async Task ExecuteAsync(CancellationToken token)
    {
        _logger.LogInformation("Starting background service API probing worker with requests delay: {Delay}", _betweenRequestsDelay);
        while (!token.IsCancellationRequested)
        {
            var startTime = DateTime.Now;
            _logger.LogDebug("Start probing at: {StartTime}", startTime);
            FireApiProbe();
            var executionTime = DateTime.Now - startTime;
            var currentDelay = _betweenRequestsDelay - executionTime;
            _logger.LogDebug("Sleeping for: {Delay}", currentDelay);
            await Task.Delay(currentDelay, token);
        }
        
        void FireApiProbe()
        {
            // ILogger<T> is thread-safe
            // https://github.com/dotnet/runtime/discussions/50695#discussioncomment-567001
            Task.Run(async () =>
            {
                await using var scope = _serviceProvider.CreateAsyncScope();
                var prober = scope.ServiceProvider.GetRequiredService<IApiProber>();
                try
                {
                    var result = await prober.ProbeAsync(token);
                    if (result.Succeed)
                    {
                        _logger.LogInformation("API probe succeed");
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