namespace InterviewTest.WebHost.ApiProber.Models;

public class ProbeResult
{
    public Exception? Exception { get; set; }
    public bool Succeed { get; }
    public string? ErrorMessage { get; }

    private ProbeResult(bool success, string? errorMessage = null, Exception? exception = null)
    {
        Succeed = success;
        Exception = exception;
        ErrorMessage = errorMessage;
    }

    public static ProbeResult Success() => new(true);
    public static ProbeResult Fail(string errorMessage, Exception? exception = null) 
        => new(false, errorMessage ?? throw new ArgumentNullException(nameof(errorMessage), ErrorMessageNull), exception);

    private const string ErrorMessageNull = "Error message must be provided when result is not successful";


}