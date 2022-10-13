namespace InterviewTest.WebHost.ApiProber.Infrastructure;

public class ProbeSettings
{
    public Uri ApiEndpoint { get; init; } = null!;
    public int Rpm { get; init; }
    public HttpMethod HttpMethod { get; init; } = null!;
}