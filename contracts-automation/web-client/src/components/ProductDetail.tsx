import React, { useState, useEffect } from 'react';
import { type ProductDto, Client } from '../contracts/api-client';

interface ProductDetailProps {
  productId: number;
}

const ProductDetail: React.FC<ProductDetailProps> = ({ productId }) => {
  const [product, setProduct] = useState<ProductDto | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const client = new Client('http://localhost:5000');
        const result = await client.getProduct(productId);
        setProduct(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Product not found');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  if (loading) return <div className="loading">Loading product...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!product) return <div className="no-data">Product not found</div>;

  return (
    <div className="product-detail">
      <h2>{product.name}</h2>
      <p className="description">{product.description}</p>
      <p className="price">${product.price?.toFixed(2)}</p>
      <p className="date">
        Created: {product.createdDate ? new Date(product.createdDate).toLocaleDateString() : 'N/A'}
      </p>
    </div>
  );
};

export default ProductDetail;
