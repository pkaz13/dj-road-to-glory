using ProductsApi.Services;
using OpenTelemetry.Resources;
using OpenTelemetry.Logs;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using Serilog;
using ILogger = Serilog.ILogger;
using OpenTelemetry;
using System.Diagnostics.Metrics;

var builder = WebApplication.CreateBuilder(args);

/////// OpenTelemetry with Serilog (see appsettings.json) //////
// builder.Logging.ClearProviders();
// builder.Host.UseSerilog((_, config) =>
//     config.ReadFrom.Configuration(builder.Configuration));

/////////////////////////////////////////////

//////// Optionally, add tracing and metrics as well //////////////////////
// builder.Services.AddOpenTelemetry()
//     .WithTracing(tracing =>
//     {
//         tracing
//             .AddAspNetCoreInstrumentation()
//             .AddHttpClientInstrumentation();
//     })
//     .WithMetrics(metrics =>
//     {
//         metrics
//             .AddAspNetCoreInstrumentation()
//             .AddHttpClientInstrumentation();
//     });

//////////////////////////////

builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource
        .AddService(serviceName: "products-api", serviceVersion: "1.0.0")
        .AddAttributes(new Dictionary<string, object>
        {
            ["deployment.environment"] = builder.Environment.EnvironmentName
        }));

// Configure logging to be exported via OpenTelemetry
// builder.Logging.ClearProviders(); //optional -> removes default logs from console in container
builder.Logging.AddOpenTelemetry(logging =>
{
    logging.IncludeFormattedMessage = true;
    logging.IncludeScopes = true;

    // optional -> adds console exporter for local development
    // if (builder.Environment.IsDevelopment())
    // {
    //     logging.AddConsoleExporter();
    // }
});

if (builder.Configuration["OTEL_EXPORTER_OTLP_ENDPOINT"] != null)
{
    builder.Services.ConfigureOpenTelemetryLoggerProvider(logging => logging.AddOtlpExporter());
    // builder.Services.ConfigureOpenTelemetryMeterProvider(metrics => metrics.AddOtlpExporter());
    // builder.Services.ConfigureOpenTelemetryTracerProvider(tracing => tracing.AddOtlpExporter());
}

// Add services to the container
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<ProductService>();

builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");

// app.UseSerilogRequestLogging();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Define the GET /products endpoint
app.MapGet("/products", async (ILogger<Program> logger, ProductService productService) =>
{
    logger.LogInformation("GET /products endpoint called.");
    try
    {
        var products = await productService.GetProductsAsync();
        logger.LogInformation("GET /products succeeded. Returning {Count} products.", products.Count());
        return Results.Ok(products);
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Error in GET /products endpoint.");
        return Results.Problem("An error occurred while retrieving products.");
    }
})
.WithName("GetProducts")
.WithOpenApi();

app.Run();
