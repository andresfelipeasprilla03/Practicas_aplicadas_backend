import React, { useState } from "react";

export default function App4({ setView }) {
  const [nombre, setNombre] = useState("");
  const [artista, setArtista] = useState("");
  const [anio, setAnio] = useState("");
  const [stock, setStock] = useState("");
  const [precio, setPrecio] = useState("");
  const [msg, setMsg] = useState("");

  const API_VINILO = "http://127.0.0.1:8000/home/vinilos/new/";
  const USUARIO_ID = 1; // tu ID de usuario fijo

  const handleSubmit = () => {
    if (!nombre.trim() || !artista.trim() || !anio || !stock || !precio) {
      setMsg("Todos los campos son obligatorios.");
      return;
    }

    fetch(API_VINILO, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre_vinilo: nombre,
        artista: artista,
        anio: parseInt(anio),
        stock: parseInt(stock),
        precio: parseFloat(precio),
        proveedor: USUARIO_ID, // siempre tu ID
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.errors) {
          setMsg("Error: " + JSON.stringify(data.errors));
        } else {
          setMsg("Vinilo creado correctamente!");
          setNombre("");
          setArtista("");
          setAnio("");
          setStock("");
          setPrecio("");
          setTimeout(() => setView("vinilo"), 1500); // vuelve a la vista de vinilos
        }
      })
      .catch((err) => {
        console.error(err);
        setMsg("Error al crear vinilo.");
      });
  };

  return (
    <div style={{ padding: "1.5rem" }}>
      <h1>Crear Vinilo</h1>

      {msg && (
        <div
          style={{
            background: "#333",
            color: "white",
            padding: "0.5rem",
            marginBottom: "1rem",
          }}
        >
          {msg}
        </div>
      )}

      <div style={{ marginBottom: "0.5rem" }}>
        <label>Nombre del vinilo:</label>
        <input
          type="text"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          style={{ marginLeft: "0.5rem", padding: "0.3rem" }}
        />
      </div>

      <div style={{ marginBottom: "0.5rem" }}>
        <label>Artista:</label>
        <input
          type="text"
          value={artista}
          onChange={(e) => setArtista(e.target.value)}
          style={{ marginLeft: "0.5rem", padding: "0.3rem" }}
        />
      </div>

      <div style={{ marginBottom: "0.5rem" }}>
        <label>Año:</label>
        <input
          type="number"
          value={anio}
          onChange={(e) => setAnio(e.target.value)}
          style={{ marginLeft: "0.5rem", padding: "0.3rem" }}
        />
      </div>

      <div style={{ marginBottom: "0.5rem" }}>
        <label>Stock:</label>
        <input
          type="number"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          style={{ marginLeft: "0.5rem", padding: "0.3rem" }}
        />
      </div>

      <div style={{ marginBottom: "0.5rem" }}>
        <label>Precio:</label>
        <input
          type="number"
          step="0.01"
          value={precio}
          onChange={(e) => setPrecio(e.target.value)}
          style={{ marginLeft: "0.5rem", padding: "0.3rem" }}
        />
      </div>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        <button onClick={handleSubmit} style={{ flex: 1 }}>
          Crear Vinilo
        </button>
        <button onClick={() => setView("vinilo")} style={{ flex: 1 }}>
          Volver a Vinilo
        </button>
      </div>
    </div>
  );
}