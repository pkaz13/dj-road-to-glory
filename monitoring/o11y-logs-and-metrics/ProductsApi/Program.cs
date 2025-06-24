using ProductsApi.Services;
using OpenTelemetry.Resources;
using OpenTelemetry.Logs;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using Serilog;
using ILogger = Serilog.ILogger;

var builder = WebApplication.CreateBuilder(args);

builder.Logging.ClearProviders();
builder.Host.UseSerilog((_, config) =>
    config.ReadFrom.Configuration(builder.Configuration));


////// Configure OpenTelemetry with default .NET logger - for some reason it doesn't work ////////

// builder.Logging.ClearProviders();
// builder.Logging.AddOpenTelemetry(options =>
// {
//     options.IncludeFormattedMessage = true;
//     options.IncludeScopes = true;
//     options.ParseStateValues = true;
//     options.SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("ProductsApi"));
// });

// if (builder.Environment.IsDevelopment())
// {
//     // In development, log to console
//     builder.Logging.AddOpenTelemetry(x => x.AddConsoleExporter());
// }

// var otlpEndpoint = builder.Configuration["OTEL_EXPORTER_OTLP_ENDPOINT"];
// if (!string.IsNullOrEmpty(otlpEndpoint))
// {
//     Console.WriteLine($"Using OTLP endpoint: {otlpEndpoint}");
//     builder.Services.Configure<OpenTelemetryLoggerOptions>(options =>
//     {
//         options.AddOtlpExporter();
//     });
// }

/////////////////////////////////////////////

//////// Optionally, add tracing and metrics as well //////////////////////
// builder.Services.AddOpenTelemetry()
//     .WithTracing(tracing =>
//     {
//         tracing
//             .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("ProductsApi"))
//             .AddAspNetCoreInstrumentation()
//             .AddHttpClientInstrumentation()
//             .AddOtlpExporter(otlpOptions =>
//             {
//                 otlpOptions.Endpoint = new Uri("http://otel-collector:4318");
//             });
//     })
//     .WithMetrics(metrics =>
//     {
//         metrics
//             .SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("ProductsApi"))
//             .AddAspNetCoreInstrumentation()
//             .AddHttpClientInstrumentation()
//             .AddOtlpExporter(otlpOptions =>
//             {
//                 otlpOptions.Endpoint = new Uri("http://otel-collector:4318");
//             });
//     });

//////////////////////////////

// Add services to the container
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<ProductService>();

builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");

app.UseSerilogRequestLogging();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Define the GET /products endpoint
app.MapGet("/products", async (ILogger logger, ProductService productService) =>
{
    logger.Information("GET /products endpoint called.");
    try
    {
        var products = await productService.GetProductsAsync();
        logger.Information("GET /products succeeded. Returning {Count} products.", products.Count());
        return Results.Ok(products);
    }
    catch (Exception ex)
    {
        logger.Error(ex, "Error in GET /products endpoint.");
        return Results.Problem("An error occurred while retrieving products.");
    }
})
.WithName("GetProducts")
.WithOpenApi();

app.Run();
