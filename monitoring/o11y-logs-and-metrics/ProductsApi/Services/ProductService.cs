using Npgsql;
using ProductsApi.Models;

namespace ProductsApi.Services;

public class ProductService(IConfiguration configuration)
{
    private readonly string _connectionString = configuration.GetConnectionString("DefaultConnection") ??
            throw new InvalidOperationException("Connection string 'DefaultConnection' not found.");

    public async Task<IEnumerable<Product>> GetProductsAsync()
    {
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
}
