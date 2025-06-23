using ProductsApi.Services;
using OpenTelemetry.Resources;
using OpenTelemetry.Logs;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;

var builder = WebApplication.CreateBuilder(args);

// Configure OpenTelemetry logging
builder.Logging.ClearProviders();
builder.Logging.AddOpenTelemetry(options =>
{
    options.IncludeFormattedMessage = true;
    options.IncludeScopes = true;
    options.ParseStateValues = true;
    options.SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("ProductsApi"));
    options.AddOtlpExporter(otlpOptions =>
    {
        otlpOptions.Endpoint = new Uri("http://otel-collector:4318"); // http endpoint
    });
});

// Optionally, add tracing and metrics as well
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

// Add services to the container
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<ProductService>();

builder.Services.AddHealthChecks();

var app = builder.Build();

app.MapHealthChecks("/health");

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Define the GET /products endpoint
app.MapGet("/products", async (ProductService productService) =>
{
    var products = await productService.GetProductsAsync();
    return Results.Ok(products);
})
.WithName("GetProducts")
.WithOpenApi();

app.Run();
