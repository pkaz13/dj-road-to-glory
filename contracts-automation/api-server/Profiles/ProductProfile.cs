using AutoMapper;
using ApiServer.Models;
using ApiServer.Contracts;

namespace ApiServer.Profiles
{
    public class ProductProfile : Profile
    {
        public ProductProfile()
        {
            CreateMap<Product, ProductDto>()
                .ForMember(dest => dest.Price, opt => opt.MapFrom(src => (double)src.Price))
                .ForMember(dest => dest.CreatedDate, opt => opt.MapFrom(src => src.CreatedDate));
                
            CreateMap<ProductDto, Product>()
                .ForMember(dest => dest.Price, opt => opt.MapFrom(src => (decimal)src.Price))
                .ForMember(dest => dest.CreatedDate, opt => opt.MapFrom(src => src.CreatedDate));
        }
    }
}
