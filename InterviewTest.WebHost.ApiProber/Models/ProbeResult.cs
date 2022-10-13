namespace InterviewTest.WebHost.ApiProber.Models;

public class ProbeResult
{
    public bool Succeed { get; }
    public string? ErrorMessage { get; }

    private ProbeResult(bool success, string? errorMessage = null)
    {
        Succeed = success;
        ErrorMessage = errorMessage;
    }

    public static ProbeResult Success() => new(true);
    public static ProbeResult Fail(string errorMessage) 
        => new(false, errorMessage ?? throw new ArgumentNullException(nameof(errorMessage), ErrorMessageNull));

    private const string ErrorMessageNull = "Error message must be provided when result is not successful";


}