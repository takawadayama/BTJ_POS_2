"use client";

import { useState } from 'react';

export default function Home() {
  const [code, setCode] = useState('');
  const [name, setName] = useState('');
  const [price, setPrice] = useState(0);
  const [message, setMessage] = useState('');

  const handleAddProduct = async () => {
    const response = await fetch('http://127.0.0.1:8000/products/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code, name, price }),
    });

    if (response.ok) {
      setMessage('Product added successfully!');
    } else {
      setMessage('Failed to add product.');
    }
  };

  return (
    <div>
      <h1>POS System</h1>
      <input
        type="text"
        placeholder="Product Code"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <input
        type="text"
        placeholder="Product Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Product Price"
        value={price}
        onChange={(e) => setPrice(parseFloat(e.target.value))}
      />
      <button onClick={handleAddProduct}>Add Product</button>
      <p>{message}</p>
    </div>
  );
}
