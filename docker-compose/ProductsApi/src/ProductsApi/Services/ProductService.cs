namespace ProductsApi.Services;

using Microsoft.EntityFrameworkCore;
using ProductsApi.Data;
using ProductsApi.Models;
using StackExchange.Redis;
using System.Text.Json;
using System.Text.Json.Serialization;

public class ProductService
{
    private readonly ApplicationDbContext _context;
    private readonly IDatabase _redis;
    private readonly TimeSpan _cacheExpiration = TimeSpan.FromMinutes(1);
    private const string _cacheKey = "products:all";

    public ProductService(ApplicationDbContext context, IConnectionMultiplexer redis)
    {
        _context = context;
        _redis = redis.GetDatabase();
    }

    public async Task<List<Product>> GetAllProductsAsync()
    {

        // Try to get from Redis cache first
        var cachedProducts = await _redis.StringGetAsync(_cacheKey);
        if (cachedProducts.HasValue)
        {
            return JsonSerializer.Deserialize<List<Product>>(cachedProducts!)!;
        }

        // If not in cache, get from database
        var products = await _context.Products
            .Include(p => p.Category)
            .OrderBy(p => p.Name)
            .ToListAsync();

        // Store in Redis cache
        var serializedProducts = JsonSerializer.Serialize(products);
        await _redis.StringSetAsync(_cacheKey, serializedProducts, _cacheExpiration);

        return products;
    }
}
