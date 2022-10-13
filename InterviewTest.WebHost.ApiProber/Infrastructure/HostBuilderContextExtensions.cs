namespace InterviewTest.WebHost.ApiProber.Infrastructure;

public static class HostBuilderContextExtensions
{
    public static ProbeSettings GetApiProbeSettings(this HostBuilderContext context)
    {
        string GetEnv(string envVariableName, string envHumanReadable)
        {
            return context.Configuration[envVariableName]
                ?? throw new ArgumentException($"{envHumanReadable} is not provided. "
                                             + $"Specify using \"{envVariableName}\" environmental variable");
        }
                    
        if (!int.TryParse(GetEnv("RPM", "RPM"), out var rpm))
        {
            throw new ArgumentException("Could not parse RPM as integer");
        }
        var apiEndpoint = new Uri( GetEnv("API_URL", "API Endpoint Url") );
                    
        var httpMethod = new HttpMethod( GetEnv("HTTP_METHOD", "Http endpoint method") );
        return new ProbeSettings() {Rpm = rpm, ApiEndpoint = apiEndpoint, HttpMethod = httpMethod};
    }
}