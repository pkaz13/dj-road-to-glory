using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace ProductsApi.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Categories",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Description = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Categories", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Products",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Name = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                    Description = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                    Price = table.Column<decimal>(type: "decimal(10,2)", nullable: false),
                    CategoryId = table.Column<int>(type: "int", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Products", x => x.Id);
                    table.ForeignKey(
                        name: "FK_Products_Categories_CategoryId",
                        column: x => x.CategoryId,
                        principalTable: "Categories",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.InsertData(
                table: "Categories",
                columns: new[] { "Id", "Description", "Name" },
                values: new object[,]
                {
                    { 1, "Electronic devices and accessories", "Electronics" },
                    { 2, "Apparel and fashion items", "Clothing" },
                    { 3, "Physical and digital books", "Books" },
                    { 4, "Home improvement and gardening supplies", "Home & Garden" },
                    { 5, "Sports equipment and accessories", "Sports" }
                });

            migrationBuilder.InsertData(
                table: "Products",
                columns: new[] { "Id", "CategoryId", "CreatedAt", "Description", "Name", "Price" },
                values: new object[,]
                {
                    { 1, 1, new DateTime(2025, 5, 16, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6010), "High-performance laptop for professionals", "Laptop Pro 15", 1299.99m },
                    { 2, 1, new DateTime(2025, 5, 21, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6010), "Noise-cancelling wireless headphones", "Wireless Headphones", 299.99m },
                    { 3, 1, new DateTime(2025, 5, 26, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6010), "Latest flagship smartphone", "Smartphone X", 899.99m },
                    { 4, 1, new DateTime(2025, 5, 31, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6010), "Next-generation gaming console", "Gaming Console", 499.99m },
                    { 5, 1, new DateTime(2025, 6, 5, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6010), "Ultra-thin tablet with stylus support", "Tablet Air", 649.99m },
                    { 6, 2, new DateTime(2025, 5, 18, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Premium cotton t-shirt", "Cotton T-Shirt", 29.99m },
                    { 7, 2, new DateTime(2025, 5, 23, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Classic fit denim jeans", "Denim Jeans", 79.99m },
                    { 8, 2, new DateTime(2025, 5, 28, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Waterproof winter jacket", "Winter Jacket", 149.99m },
                    { 9, 2, new DateTime(2025, 6, 2, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Lightweight running shoes", "Running Shoes", 119.99m },
                    { 10, 2, new DateTime(2025, 6, 7, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Comfortable casual dress", "Casual Dress", 89.99m },
                    { 11, 3, new DateTime(2025, 5, 20, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Complete guide to software development", "Programming Guide", 49.99m },
                    { 12, 3, new DateTime(2025, 5, 25, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Bestselling fiction novel", "Fiction Novel", 19.99m },
                    { 13, 3, new DateTime(2025, 5, 30, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6020), "Healthy cooking recipes", "Cookbook", 34.99m },
                    { 14, 3, new DateTime(2025, 6, 4, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "World history comprehensive guide", "History Book", 39.99m },
                    { 15, 3, new DateTime(2025, 6, 9, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Advanced science concepts", "Science Textbook", 89.99m },
                    { 16, 4, new DateTime(2025, 5, 22, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Complete gardening tools set", "Garden Tools Set", 79.99m },
                    { 17, 4, new DateTime(2025, 5, 27, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Decorative ceramic plant pot", "Indoor Plant Pot", 24.99m },
                    { 18, 4, new DateTime(2025, 6, 1, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Electric lawn mower", "Lawn Mower", 299.99m },
                    { 19, 4, new DateTime(2025, 6, 6, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Weather-resistant patio set", "Outdoor Furniture", 499.99m },
                    { 20, 4, new DateTime(2025, 6, 11, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Solar-powered garden lighting", "LED Garden Lights", 59.99m },
                    { 21, 5, new DateTime(2025, 5, 24, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Professional tennis racket", "Tennis Racket", 149.99m },
                    { 22, 5, new DateTime(2025, 5, 29, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6030), "Official size basketball", "Basketball", 39.99m },
                    { 23, 5, new DateTime(2025, 6, 3, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6040), "Non-slip exercise yoga mat", "Yoga Mat", 29.99m },
                    { 24, 5, new DateTime(2025, 6, 8, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6040), "Waterproof fitness tracker", "Fitness Tracker", 199.99m },
                    { 25, 5, new DateTime(2025, 6, 13, 18, 27, 46, 39, DateTimeKind.Utc).AddTicks(6040), "Adjustable dumbbells set", "Dumbbells Set", 299.99m }
                });

            migrationBuilder.CreateIndex(
                name: "IX_Categories_Name",
                table: "Categories",
                column: "Name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Products_CategoryId",
                table: "Products",
                column: "CategoryId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Products");

            migrationBuilder.DropTable(
                name: "Categories");
        }
    }
}
