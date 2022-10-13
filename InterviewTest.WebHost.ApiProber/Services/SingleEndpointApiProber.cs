using InterviewTest.WebHost.ApiProber.Infrastructure;
using InterviewTest.WebHost.ApiProber.Interfaces;
using InterviewTest.WebHost.ApiProber.Models;

namespace InterviewTest.WebHost.ApiProber.Services;

public class SingleEndpointApiProber: IApiProber
{
    private readonly ILogger<SingleEndpointApiProber> _logger;
    private readonly HttpClient _client;
    private readonly Uri _endpoint;
    private readonly HttpMethod _method;

    public SingleEndpointApiProber(ILogger<SingleEndpointApiProber> logger, 
                                   HttpClient client, 
                                   ProbeSettings settings)
    {
        _logger = logger;
        _client = client;
        _endpoint = settings.ApiEndpoint;
        _method = settings.HttpMethod;
    }


    public async Task<ProbeResult> ProbeAsync(CancellationToken token = default)
    {
        try
        {
            using var message = new HttpRequestMessage(_method, _endpoint);
            _logger.LogDebug("Created HttpRequestMessage");
            _logger.LogDebug("Start HTTP request to: {Url}", _endpoint);
            using var response = await _client.SendAsync(message, token);
            _logger.LogDebug("End HTTP request to: {Url}", _endpoint);
            if (response.IsSuccessStatusCode)
            {
                return ProbeResult.Success();
            }
            return ProbeResult.Fail($"Returned not success status code: {response.StatusCode}");
        }
        catch (TaskCanceledException canceledException)
        {
            return ProbeResult.Fail("Task was cancelled", canceledException);
        }
        catch (HttpRequestException requestException)
        {
            _logger.LogWarning(requestException, "HttpRequestException was thrown during sending request");
            return ProbeResult.Fail("Error occured during HTTP request", requestException);
        }
    }
}