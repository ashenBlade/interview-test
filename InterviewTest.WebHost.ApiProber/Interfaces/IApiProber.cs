using InterviewTest.WebHost.ApiProber.Models;

namespace InterviewTest.WebHost.ApiProber.Interfaces;

public interface IApiProber
{
    Task<ProbeResult> ProbeAsync();
}