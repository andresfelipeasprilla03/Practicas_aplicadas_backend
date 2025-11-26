import React from "react";

export default function App3({ cart, quitar, setView }) {
  // Calcular el precio total
  const total = cart.reduce((sum, item) => sum + (item.price || 0) * (item.qty || 1), 0);

  return (
    <div style={{ padding: "1.5rem" }}>
      <h1>Carrito de Compras</h1>

      {cart.length === 0 ? (
        <p>El carrito está vacío</p>
      ) : (
        <ul>
          {cart.map((item, index) => (
            <li key={index} style={{ marginBottom: "0.5rem" }}>
              {item.name || item.type} - ${item.price} x {item.qty || 1}{" "}
              <button onClick={() => quitar(index)}>Quitar</button>
            </li>
          ))}
        </ul>
      )}

      <h2>Total: ${total.toFixed(2)}</h2>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
      <button style={{ flex: 1 }} onClick={() => setLocalView("catalog")}>
          Volver al Catálogo
        </button>
        <button style={{ flex: 1 }} onClick={() => alert("Pago realizado con éxito!")}>
          Pagar
        </button>
      </div>
    </div>
  );
}