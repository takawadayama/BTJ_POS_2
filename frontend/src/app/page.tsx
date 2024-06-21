"use client";

import { useState, useEffect } from 'react';

interface Product {
  id: number;
  code: string;
  name: string;
  price: number;
}

interface CartItem {
  product: Product;
  quantity: number;
}

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [message, setMessage] = useState('');
  const [productCode, setProductCode] = useState('');
  const [productName, setProductName] = useState('');
  const [productPrice, setProductPrice] = useState(0);
  const [quantity, setQuantity] = useState(0);

  useEffect(() => {
    // バックエンドから商品データを取得する処理
    const fetchProducts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/products/');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
      } catch (error) {
        console.error("Failed to fetch products:", error);
        setMessage("Failed to fetch products.");
      }
    };

    fetchProducts();
  }, []);

  const handleLoadProduct = () => {
    const product = products.find(p => p.code === productCode);
    if (product) {
      setProductName(product.name);
      setProductPrice(product.price);
    } else {
      setProductName('商品がマスタ未登録です');
      setProductPrice(0);
    }
  };

  const handleAddToCart = () => {
    const product = products.find(p => p.code === productCode);
    if (product && quantity > 0) {
      const existingItem = cart.find(item => item.product.id === product.id);
      if (existingItem) {
        existingItem.quantity += quantity;
        setCart([...cart]);
      } else {
        setCart([...cart, { product, quantity }]);
      }
      setProductCode('');
      setProductName('');
      setProductPrice(0);
      setQuantity(0);
    }
  };

  const handlePurchase = async () => {
    const totalAmount = cart.reduce((total, item) => total + item.product.price * item.quantity, 0);

    const transaction = {
      datetime: new Date().toISOString(),  // 現在の日時をISO形式で設定
      emp_code: 'EMP001', // 実際の値に置き換える
      store_code: 'STR001', // 実際の値に置き換える
      pos_no: 'POS001', // 実際の値に置き換える
      total_amt: totalAmount,
      details: cart.map(item => ({
        product_code: item.product.code,
        product_name: item.product.name,
        product_price: item.product.price,
        quantity: item.quantity
      }))
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/transactions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(transaction),
      });

      if (response.ok) {
        setMessage('Purchase completed successfully!');
        setCart([]);
      } else {
        setMessage('Failed to complete purchase.');
      }
    } catch (error) {
      console.error("Failed to complete purchase:", error);
      setMessage("Failed to complete purchase.");
    }
  };

  const totalExcludingTax: number = cart.reduce((total, item) => total + item.product.price * item.quantity, 0);
  const totalIncludingTax: number = Math.round(totalExcludingTax * 1.1); // 10%の消費税を追加

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 p-8">
      <h1 className="text-4xl font-bold text-center text-gray-100 mb-8">びあPOS</h1>
      <div className="flex flex-col md:flex-row justify-between gap-8">
        <div className="bg-gray-800 rounded-lg shadow-lg p-6 max-w-md mx-auto w-full">
          <div className="mb-4">
            <input
              type="text"
              placeholder="商品コード"
              value={productCode}
              onChange={(e) => setProductCode(e.target.value)}
              className="w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-200"
            />
            <button
              onClick={handleLoadProduct}
              className="w-full mt-2 bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700"
            >
              商品コード読み込み
            </button>
          </div>
          <div className="mb-4">
            <input
              type="text"
              placeholder="商品名"
              value={productName}
              readOnly
              className="w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-400"
            />
          </div>
          <div className="mb-4">
            <input
              type="text"
              placeholder="単価"
              value={productPrice ? `${productPrice}円` : ''}
              readOnly
              className="w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-400"
            />
          </div>
          <div className="mb-4">
            <input
              type="number"
              min="0"
              placeholder="数量"
              value={quantity.toString()}
              onChange={(e) => setQuantity(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-gray-600 rounded-md bg-gray-700 text-gray-200"
            />
            <button
              onClick={handleAddToCart}
              className="w-full mt-2 bg-green-600 text-white py-2 rounded-md hover:bg-green-700"
            >
              カートへ追加
            </button>
          </div>
        </div>
        <div className="bg-gray-800 rounded-lg shadow-lg p-6 max-w-md mx-auto w-full">
          <h2 className="text-2xl font-bold text-center mb-4">購入リスト</h2>
          <ul className="mb-4">
            {cart.map(item => (
              <li key={item.product.id} className="mb-2">
                {item.product.name} - {item.quantity} x {item.product.price} = {item.quantity * item.product.price}円
              </li>
            ))}
          </ul>
          <h3 className="text-xl font-bold">合計金額（税抜）: {totalExcludingTax}円</h3>
          <h3 className="text-xl font-bold">合計金額（税込）: {totalIncludingTax}円</h3>
          <button
            onClick={handlePurchase}
            className="w-full mt-4 bg-red-600 text-white py-2 rounded-md hover:bg-red-700"
          >
            購入
          </button>
          <p className="text-center mt-4 text-red-500 bg-red-100 rounded-md p-2">{message}</p>
        </div>
      </div>
    </div>
  );
}
