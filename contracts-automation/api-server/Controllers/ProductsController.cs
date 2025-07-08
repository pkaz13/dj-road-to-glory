using Microsoft.AspNetCore.Mvc;
using AutoMapper;
using ApiServer.Models;
using ApiServer.Contracts;

namespace ApiServer.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ProductsController(IMapper mapper) : ControllerBase
    {
        private readonly IMapper _mapper = mapper;
        private static readonly List<Product> _products = new()
        {
            new Product { Id = 1, Name = "Gaming Laptop", Description = "High-performance gaming laptop", Price = 1299.99m, CreatedDate = DateTime.Now.AddDays(-10), IsActive = true },
            new Product { Id = 2, Name = "Wireless Mouse", Description = "Ergonomic wireless mouse", Price = 29.99m, CreatedDate = DateTime.Now.AddDays(-5), IsActive = true },
            new Product { Id = 3, Name = "Mechanical Keyboard", Description = "RGB mechanical keyboard", Price = 149.99m, CreatedDate = DateTime.Now.AddDays(-3), IsActive = true }
        };

        [HttpGet]
        public ActionResult<IEnumerable<ProductDto>> GetProducts()
        {
            var activeProducts = _products.Where(p => p.IsActive).ToList();
            var productDtos = _mapper.Map<IEnumerable<ProductDto>>(activeProducts);

            return Ok(productDtos);
        }

        [HttpGet("{id}")]
        public ActionResult<ProductDto> GetProduct(int id)
        {
            var product = _products.FirstOrDefault(p => p.Id == id && p.IsActive);
            if (product == null)
            {
                return NotFound();
            }

            var productDto = _mapper.Map<ProductDto>(product);
            
            return Ok(productDto);
        }
    }
}
