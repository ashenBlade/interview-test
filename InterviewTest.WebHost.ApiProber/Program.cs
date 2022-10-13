using InterviewTest.WebHost.ApiProber.Infrastructure;
using InterviewTest.WebHost.ApiProber.Interfaces;
using InterviewTest.WebHost.ApiProber.Services;
using InterviewTest.WebHost.ApiProber.Workers;

var host = Host.CreateDefaultBuilder(args)
               .ConfigureServices((context, services) =>
                {
                    var settings = context.GetApiProbeSettings();
                    services.AddSingleton(settings);
                    services.AddScoped<HttpClient>();
                    services.AddScoped<IApiProber, SingleEndpointApiProber>();
                    services.AddHostedService<ApiProberWorker>();
                })
               .Build();

await host.RunAsync();