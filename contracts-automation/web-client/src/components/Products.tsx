import React, { useState, useEffect } from 'react';
import { type ProductDto, Client } from '../contracts/api-client';

const Products: React.FC = () => {
  const [products, setProducts] = useState<ProductDto[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const client = new Client('http://localhost:5050');
        const result = await client.getProducts();
        setProducts(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <div className="loading">Loading products...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!products.length) return <div className="no-data">No products found</div>;

  return (
    <div className="products-container">
      <h2>Products</h2>
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <p className="description">{product.description}</p>
            <p className="price">${product.price?.toFixed(2)}</p>
            <small className="date">
              Created: {product.createdDate ? new Date(product.createdDate).toLocaleDateString() : 'N/A'}
            </small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Products;
