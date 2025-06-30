using Npgsql;
using ProductsApi.Models;
using System.Diagnostics;

namespace ProductsApi.Services;

public class ProductService(IConfiguration configuration, ActivitySource activitySource)
{
    private readonly string _connectionString = configuration.GetConnectionString("DefaultConnection") ??
            throw new InvalidOperationException("Connection string 'DefaultConnection' not found.");
    private readonly ActivitySource _activitySource = activitySource;

    public async Task<IEnumerable<Product>> GetProductsAsync()
    {
        using var activity = _activitySource.StartActivity("GetProductsAsync");
        activity?.SetTag("db.system", "postgresql");
        activity?.SetTag("db.operation", "SELECT");
        activity?.SetTag("db.statement", "SELECT ... FROM products JOIN categories ...");

        var products = new List<Product>();
        
        using var connection = new NpgsqlConnection(_connectionString);
        await connection.OpenAsync();
        
        using var command = new NpgsqlCommand(
            @"SELECT p.id, p.name, p.description, p.price, p.category_id, 
                     c.name as category_name, c.description as category_description
              FROM products p
              JOIN categories c ON p.category_id = c.id", connection);
        
        using var reader = await command.ExecuteReaderAsync();
        
        while (await reader.ReadAsync())
        {
            products.Add(new Product
            {
                Id = reader.GetInt32(0),
                Name = reader.GetString(1),
                Description = reader.GetString(2),
                Price = reader.GetDecimal(3),
                CategoryId = reader.GetInt32(4),
                Category = new Category
                {
                    Id = reader.GetInt32(4),
                    Name = reader.GetString(5),
                    Description = reader.GetString(6)
                }
            });
        }
        
        return products;
    }

    public async Task<Product?> GetProductByIdAsync(int productId)
    {
        using var activity = _activitySource.StartActivity("GetProductByIdAsync");
        activity?.SetTag("db.system", "postgresql");
        activity?.SetTag("db.operation", "SELECT");
        activity?.SetTag("db.statement", "SELECT ... FROM products JOIN categories ... WHERE p.id = @id");
        activity?.SetTag("db.sql.parameters", $"productId={productId}");

        using var connection = new NpgsqlConnection(_connectionString);
        await connection.OpenAsync();

        using var command = new NpgsqlCommand(
            @"SELECT p.id, p.name, p.description, p.price, p.category_id, 
                     c.name as category_name, c.description as category_description
              FROM products p
              JOIN categories c ON p.category_id = c.id
              WHERE p.id = @id", connection);
        command.Parameters.AddWithValue("@id", productId);

        using var reader = await command.ExecuteReaderAsync();
        if (await reader.ReadAsync())
        {
            return new Product
            {
                Id = reader.GetInt32(0),
                Name = reader.GetString(1),
                Description = reader.GetString(2),
                Price = reader.GetDecimal(3),
                CategoryId = reader.GetInt32(4),
                Category = new Category
                {
                    Id = reader.GetInt32(4),
                    Name = reader.GetString(5),
                    Description = reader.GetString(6)
                }
            };
        }
        
        return null;
    }
}
