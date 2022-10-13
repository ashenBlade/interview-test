using InterviewTest.WebHost.ApiProber.Interfaces;
using InterviewTest.WebHost.ApiProber.Services;
using InterviewTest.WebHost.ApiProber.Workers;

IHost host = Host.CreateDefaultBuilder(args)
                 .ConfigureServices(services =>
                  {
                      services.AddScoped<HttpClient>();
                      services.AddScoped<IApiProber>(s =>
                                                         new SingleEndpointApiProber(s.GetRequiredService<ILogger<SingleEndpointApiProber>>(), 
                                                                                     s.GetRequiredService<HttpClient>(),
                                                                                     new Uri("https://google.com"), 
                                                                                     HttpMethod.Get));
                      services.AddHostedService<ApiProberWorker>();
                  })
                 .Build();

await host.RunAsync();