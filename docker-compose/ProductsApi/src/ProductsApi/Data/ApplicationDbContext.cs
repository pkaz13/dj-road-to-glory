namespace ProductsApi.Data;

using Microsoft.EntityFrameworkCore;
using ProductsApi.Models;

public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : DbContext(options)
{
    public DbSet<Product> Products { get; set; }
    public DbSet<Category> Categories { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Configure Product entity
        modelBuilder.Entity<Product>(entity =>
        {
            entity.HasKey(e => e.Id);
            // Property configuration moved to data annotations
            // Create index on CategoryId for better join performance
            entity.HasIndex(e => e.CategoryId);
            // Configure foreign key relationship
            entity.HasOne(e => e.Category)
                  .WithMany(c => c.Products)
                  .HasForeignKey(e => e.CategoryId)
                  .OnDelete(DeleteBehavior.Restrict);
        });

        // Configure Category entity
        modelBuilder.Entity<Category>(entity =>
        {
            entity.HasKey(e => e.Id);
            // Property configuration moved to data annotations
            // Create unique index on category name
            entity.HasIndex(e => e.Name).IsUnique();
        });

        // Seed Categories data
        modelBuilder.Entity<Category>().HasData(
            new Category { Id = 1, Name = "Electronics", Description = "Electronic devices and accessories" },
            new Category { Id = 2, Name = "Clothing", Description = "Apparel and fashion items" },
            new Category { Id = 3, Name = "Books", Description = "Physical and digital books" },
            new Category { Id = 4, Name = "Home & Garden", Description = "Home improvement and gardening supplies" },
            new Category { Id = 5, Name = "Sports", Description = "Sports equipment and accessories" }
        );

        // Seed Products data
        modelBuilder.Entity<Product>().HasData(
            // Electronics
            new Product { Id = 1, Name = "Laptop Pro 15", Description = "High-performance laptop for professionals", Price = 1299.99m, CategoryId = 1, CreatedAt = DateTime.UtcNow.AddDays(-30) },
            new Product { Id = 2, Name = "Wireless Headphones", Description = "Noise-cancelling wireless headphones", Price = 299.99m, CategoryId = 1, CreatedAt = DateTime.UtcNow.AddDays(-25) },
            new Product { Id = 3, Name = "Smartphone X", Description = "Latest flagship smartphone", Price = 899.99m, CategoryId = 1, CreatedAt = DateTime.UtcNow.AddDays(-20) },
            new Product { Id = 4, Name = "Gaming Console", Description = "Next-generation gaming console", Price = 499.99m, CategoryId = 1, CreatedAt = DateTime.UtcNow.AddDays(-15) },
            new Product { Id = 5, Name = "Tablet Air", Description = "Ultra-thin tablet with stylus support", Price = 649.99m, CategoryId = 1, CreatedAt = DateTime.UtcNow.AddDays(-10) },

            // Clothing
            new Product { Id = 6, Name = "Cotton T-Shirt", Description = "Premium cotton t-shirt", Price = 29.99m, CategoryId = 2, CreatedAt = DateTime.UtcNow.AddDays(-28) },
            new Product { Id = 7, Name = "Denim Jeans", Description = "Classic fit denim jeans", Price = 79.99m, CategoryId = 2, CreatedAt = DateTime.UtcNow.AddDays(-23) },
            new Product { Id = 8, Name = "Winter Jacket", Description = "Waterproof winter jacket", Price = 149.99m, CategoryId = 2, CreatedAt = DateTime.UtcNow.AddDays(-18) },
            new Product { Id = 9, Name = "Running Shoes", Description = "Lightweight running shoes", Price = 119.99m, CategoryId = 2, CreatedAt = DateTime.UtcNow.AddDays(-13) },
            new Product { Id = 10, Name = "Casual Dress", Description = "Comfortable casual dress", Price = 89.99m, CategoryId = 2, CreatedAt = DateTime.UtcNow.AddDays(-8) },

            // Books
            new Product { Id = 11, Name = "Programming Guide", Description = "Complete guide to software development", Price = 49.99m, CategoryId = 3, CreatedAt = DateTime.UtcNow.AddDays(-26) },
            new Product { Id = 12, Name = "Fiction Novel", Description = "Bestselling fiction novel", Price = 19.99m, CategoryId = 3, CreatedAt = DateTime.UtcNow.AddDays(-21) },
            new Product { Id = 13, Name = "Cookbook", Description = "Healthy cooking recipes", Price = 34.99m, CategoryId = 3, CreatedAt = DateTime.UtcNow.AddDays(-16) },
            new Product { Id = 14, Name = "History Book", Description = "World history comprehensive guide", Price = 39.99m, CategoryId = 3, CreatedAt = DateTime.UtcNow.AddDays(-11) },
            new Product { Id = 15, Name = "Science Textbook", Description = "Advanced science concepts", Price = 89.99m, CategoryId = 3, CreatedAt = DateTime.UtcNow.AddDays(-6) },

            // Home & Garden
            new Product { Id = 16, Name = "Garden Tools Set", Description = "Complete gardening tools set", Price = 79.99m, CategoryId = 4, CreatedAt = DateTime.UtcNow.AddDays(-24) },
            new Product { Id = 17, Name = "Indoor Plant Pot", Description = "Decorative ceramic plant pot", Price = 24.99m, CategoryId = 4, CreatedAt = DateTime.UtcNow.AddDays(-19) },
            new Product { Id = 18, Name = "Lawn Mower", Description = "Electric lawn mower", Price = 299.99m, CategoryId = 4, CreatedAt = DateTime.UtcNow.AddDays(-14) },
            new Product { Id = 19, Name = "Outdoor Furniture", Description = "Weather-resistant patio set", Price = 499.99m, CategoryId = 4, CreatedAt = DateTime.UtcNow.AddDays(-9) },
            new Product { Id = 20, Name = "LED Garden Lights", Description = "Solar-powered garden lighting", Price = 59.99m, CategoryId = 4, CreatedAt = DateTime.UtcNow.AddDays(-4) },

            // Sports
            new Product { Id = 21, Name = "Tennis Racket", Description = "Professional tennis racket", Price = 149.99m, CategoryId = 5, CreatedAt = DateTime.UtcNow.AddDays(-22) },
            new Product { Id = 22, Name = "Basketball", Description = "Official size basketball", Price = 39.99m, CategoryId = 5, CreatedAt = DateTime.UtcNow.AddDays(-17) },
            new Product { Id = 23, Name = "Yoga Mat", Description = "Non-slip exercise yoga mat", Price = 29.99m, CategoryId = 5, CreatedAt = DateTime.UtcNow.AddDays(-12) },
            new Product { Id = 24, Name = "Fitness Tracker", Description = "Waterproof fitness tracker", Price = 199.99m, CategoryId = 5, CreatedAt = DateTime.UtcNow.AddDays(-7) },
            new Product { Id = 25, Name = "Dumbbells Set", Description = "Adjustable dumbbells set", Price = 299.99m, CategoryId = 5, CreatedAt = DateTime.UtcNow.AddDays(-2) }
        );
    }
}

