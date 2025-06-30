using ProductsApi.Services;
using OpenTelemetry.Resources;
using OpenTelemetry.Logs;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using Serilog;
using ILogger = Serilog.ILogger;
using OpenTelemetry;
using System.Diagnostics.Metrics;
using System.Diagnostics;

var builder = WebApplication.CreateBuilder(args);

/////// OpenTelemetry with Serilog (see appsettings.json) //////
// builder.Logging.ClearProviders();
// builder.Host.UseSerilog((_, config) =>
//     config.ReadFrom.Configuration(builder.Configuration));

var meter = new Meter("ProductsApi");
var requestsCounter = meter.CreateCounter<int>("api.requests.count", description: "Number of requests to the the api");
var requestDuration = meter.CreateHistogram<double>("api.request.duration", 
    unit: "ms", description: "Duration of API requests in milliseconds");
var activeConnections = meter.CreateUpDownCounter<int>("api.active.connections", 
    description: "Number of active connections");

var activitySource = new ActivitySource("ProductsApi");
builder.Services.AddSingleton(activitySource);

builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource
        .AddService(serviceName: "products-api", serviceVersion: "1.0.0")
        .AddAttributes(new Dictionary<string, object>
        {
            ["deployment.environment"] = builder.Environment.EnvironmentName
        }))
    .WithMetrics(metrics =>
    {
        metrics
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddMeter(meter.Name)
            .AddView("api.request.duration", new ExplicitBucketHistogramConfiguration{
                Boundaries = [50, 100, 500, 1000, 2000, 2500, 5000, 10000]
            });
    })
    .WithTracing(tracing =>
    {
        tracing
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddSource(activitySource.Name);
    });

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
    builder.Services.ConfigureOpenTelemetryMeterProvider(metrics => metrics.AddOtlpExporter());
    builder.Services.ConfigureOpenTelemetryTracerProvider(tracing => tracing.AddOtlpExporter());
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

// Custom middleware to track active connections
app.Use(async (context, next) =>
{
    activeConnections.Add(1);
    var stopwatch = Stopwatch.StartNew();
    
    try
    {
        await next();
    }
    finally
    {
        stopwatch.Stop();
        activeConnections.Add(-1);
        requestDuration.Record(stopwatch.ElapsedMilliseconds, 
            new("endpoint", context.Request.Path),
            new("method", context.Request.Method),
            new("status_code", context.Response.StatusCode.ToString()));
    }
});

// Define the GET /products endpoint
app.MapGet("/products", async (ILogger<Program> logger, ProductService productService) =>
{
    logger.LogInformation("GET /products endpoint called.");
    try
    {
        await Task.Delay(TimeSpan.FromSeconds(2)); //simulate longer fetch from database
        var products = await productService.GetProductsAsync();
        logger.LogInformation("GET /products succeeded. Returning {Count} products.", products.Count());

        requestsCounter.Add(1, new("endpoint", "GET /products"), new("method", "GET"), new("status", "200"));
        return Results.Ok(products);
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Error in GET /products endpoint.");
        requestsCounter.Add(1, new("endpoint", "GET /products"), new("method", "GET"), new("status", "500"));

        return Results.Problem("An error occurred while retrieving products.");
    }
})
.WithName("GetProducts")
.WithOpenApi();

app.MapGet("/products/{productId:int}", async (ILogger<Program> logger, ProductService productService, int productId) =>
{
    logger.LogInformation("GET /products/{ProductId} endpoint called.", productId);
    try
    {
        var product = await productService.GetProductByIdAsync(productId);
        if (product is null)
        {
            logger.LogWarning("Product with ID {ProductId} not found.", productId);
            requestsCounter.Add(1, new("endpoint", $"GET /products/{productId}"), new("method", "GET"), new("status", "404"));

            return Results.NotFound($"Product with ID {productId} not found.");
        }

        logger.LogInformation("GET /product/{ProductId} succeeded.", productId);
        requestsCounter.Add(1, new("endpoint", $"GET /products/{productId}"), new("method", "GET"), new("status", "200"));

        return Results.Ok(product);
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Error in GET /products/{ProductId} endpoint.", productId);
        requestsCounter.Add(1, new("endpoint", $"GET /products/{productId}"), new("method", "GET"), new("status", "500"));
        
        return Results.Problem($"An error occurred while retrieving product with ID {productId}.");
    }
})
.WithName("GetProductById")
.WithOpenApi();

app.Run();
