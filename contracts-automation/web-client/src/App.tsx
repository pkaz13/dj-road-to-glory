import { useState } from 'react';
import Products from './components/Products';
import ProductDetail from './components/ProductDetail';
import './App.css';

function App() {
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Product Management System</h1>
        <p>Built with Contract-First API Development</p>
      </header>
      <main className="App-main">
        <div className="navigation">
          <button 
            onClick={() => setSelectedProductId(null)}
            className={selectedProductId === null ? 'active' : ''}
          >
            All Products
          </button>
          <button 
            onClick={() => setSelectedProductId(1)}
            className={selectedProductId === 1 ? 'active' : ''}
          >
            Product 1
          </button>
          <button 
            onClick={() => setSelectedProductId(2)}
            className={selectedProductId === 2 ? 'active' : ''}
          >
            Product 2
          </button>
        </div>
        
        {selectedProductId === null ? (
          <Products />
        ) : (
          <ProductDetail productId={selectedProductId} />
        )}
      </main>
    </div>
  );
}

export default App;
