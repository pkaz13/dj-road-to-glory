using Microsoft.EntityFrameworkCore;
using ProductsApi.Data;
using ProductsApi.Services;
using StackExchange.Redis;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Add Entity Framework
builder.Services.AddDbContext<ApplicationDbContext>(options =>
{
    var connString = builder.Configuration.GetConnectionString("DefaultConnection");
    options.UseSqlServer(connString);
});

// Add Redis
builder.Services.AddSingleton<IConnectionMultiplexer>(provider =>
{
    var connectionString = builder.Configuration.GetConnectionString("Redis") 
        ?? throw new InvalidOperationException("Redis connection string is not configured");
    return ConnectionMultiplexer.Connect(connectionString);
});

builder.Services.AddScoped<ProductService>();

var app = builder.Build();


// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

// Database initialization - only when database doesn't exist
await InitializeDatabaseAsync(app.Services);

// Configure endpoints
app.MapGet("/products", async (ProductService productService) =>
{
    var products = await productService.GetAllProductsAsync();
    return Results.Ok(products);
})
.WithName("GetProducts")
.WithOpenApi();

app.Run();

async Task InitializeDatabaseAsync(IServiceProvider services)
{
    var logger = services.GetRequiredService<ILogger<Program>>();
    using var scope = services.CreateScope();
    var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    
    try
    {
        // Check if database can be connected to (this will return false if database doesn't exist)
        var canConnect = await context.Database.CanConnectAsync();
        
        if (!canConnect)
        {
            logger.LogInformation("Database does not exist. Creating database and applying migrations...");
            
            // This will create the database and apply all migrations
            await context.Database.MigrateAsync();
            
            logger.LogInformation("Database created and migrations applied successfully.");
        }
        else
        {
            // Database exists, check if there are pending migrations
            var pendingMigrations = await context.Database.GetPendingMigrationsAsync();
            
            if (pendingMigrations.Any())
            {
                logger.LogInformation("Applying pending migrations...");
                await context.Database.MigrateAsync();
                logger.LogInformation("Pending migrations applied successfully.");
            }
            else
            {
                logger.LogInformation("Database is up to date. No migrations needed.");
            }
        }
    }
    catch (Exception ex)
    {
        logger.LogError(ex, "Database initialization failed");
        throw;
    }
}
