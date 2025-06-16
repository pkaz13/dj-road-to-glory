namespace ProductsApi.Models;
using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

public class Category
{
    public int Id { get; set; }
    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;
    [MaxLength(500)]
    public string Description { get; set; } = string.Empty;
    [JsonIgnore]
    public ICollection<Product> Products { get; set; } = [];
}