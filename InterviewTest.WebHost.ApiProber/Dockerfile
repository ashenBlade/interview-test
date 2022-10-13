FROM mcr.microsoft.com/dotnet/runtime:6.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY ["InterviewTest.WebHost.ApiProber/InterviewTest.WebHost.ApiProber.csproj", "InterviewTest.WebHost.ApiProber/"]
RUN dotnet restore "InterviewTest.WebHost.ApiProber/InterviewTest.WebHost.ApiProber.csproj"
COPY . .
WORKDIR "/src/InterviewTest.WebHost.ApiProber"
RUN dotnet build "InterviewTest.WebHost.ApiProber.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "InterviewTest.WebHost.ApiProber.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "InterviewTest.WebHost.ApiProber.dll"]
