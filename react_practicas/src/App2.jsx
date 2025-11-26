import React, { useEffect, useState } from "react";
import App3 from "./App3";
import App4 from "./App4";

export default function App2({ setView }) {
  const [catalog, setCatalog] = useState({ songs: [], vinyls: [] });
  const [cart, setCart] = useState([]);
  const [msg, setMsg] = useState("");
  const [localView, setLocalView] = useState("catalog"); // "catalog", "cart", "upload"

  const API_CANCIONES = "http://127.0.0.1:8000/home/canciones/";
  const API_VINILOS = "http://127.0.0.1:8000/home/vinilos/";
  const API_CARRITO_ITEM = "http://127.0.0.1:8000/home/carrito-items/nuevo/";

  const carritoId = 1; // Ajusta según el carrito del usuario

  // Cargar datos desde la DB
  useEffect(() => {
    fetch(API_CANCIONES)
      .then((res) => res.json())
      .then((data) => {
        let songs = data.object_list;
        if (typeof songs === "string") songs = JSON.parse(songs);
        songs = songs.map((c) => ({
          id: c.pk,
          name: c.fields.nombre_cancion,
          artist: c.fields.artista,
          duration: c.fields.duracion_segundos
            ? `${Math.floor(c.fields.duracion_segundos / 60)}:${c.fields.duracion_segundos % 60}`
            : "N/A",
          price: c.fields.precio || 0,
        }));
        setCatalog((prev) => ({ ...prev, songs }));
      })
      .catch(() => setMsg("Error al cargar canciones"));

    fetch(API_VINILOS)
      .then((res) => res.json())
      .then((data) => {
        let vinyls = data.object_list;
        if (typeof vinyls === "string") vinyls = JSON.parse(vinyls);
        vinyls = vinyls.map((v) => ({
          id: v.pk,
          name: v.fields.nombre_vinilo,
          artist: v.fields.artista,
          year: v.fields.anio,
          stock: v.fields.stock,
          price: v.fields.precio,
        }));
        setCatalog((prev) => ({ ...prev, vinyls }));
      })
      .catch(() => setMsg("Error al cargar vinilos"));
  }, []);

  const agregar = (item) => {
    setCart((prev) => [...prev, item]);
    setMsg("Agregado al carrito correctamente.");
    setTimeout(() => setMsg(""), 2000);

    fetch(API_CARRITO_ITEM, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        carrito: carritoId,
        cancion: item.type === "mp3" ? item.id : null,
        vinilo: item.type === "vinyl" ? item.id : null,
        cantidad: item.qty || 1,
      }),
    })
      .then((res) => res.json())
      .then((data) => console.log("Item agregado al backend:", data))
      .catch((err) => console.error("Error agregando item al backend:", err));
  };

  const quitar = (index) => {
    setCart((prev) => prev.filter((_, i) => i !== index));
  };

  // ---------------- RENDERS ----------------
  if (localView === "cart") {
    return <App3 setLocalView={setLocalView} cart={cart} quitar={quitar} />;
  }

  if (localView === "upload") {
    return <App4 setLocalView={setLocalView} />;
  }

  // Catálogo
  return (
    <div style={{ padding: "1.5rem" }}>
      <h1>Catálogo</h1>

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

      <section style={{ marginBottom: "2rem" }}>
        <h2>Canciones</h2>
        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          {catalog.songs.map((song) => (
            <div
              key={song.id}
              style={{
                width: 220,
                border: "1px solid #ccc",
                padding: "0.7rem",
                borderRadius: 6,
              }}
            >
              <strong>{song.name}</strong>
              <div>Artista: {song.artist}</div>
              <div>Duración: {song.duration}</div>
              <div>Precio: ${song.price}</div>
              <button
                style={{ marginTop: 8 }}
                onClick={() => agregar({ ...song, type: "mp3" })}
              >
                Agregar al carrito
              </button>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Vinilos</h2>
        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          {catalog.vinyls.map((vinyl) => (
            <div
              key={vinyl.id}
              style={{
                width: 220,
                border: "1px solid #ccc",
                padding: "0.7rem",
                borderRadius: 6,
              }}
            >
              <strong>{vinyl.name}</strong>
              <div>Artista: {vinyl.artist}</div>
              <div>Año: {vinyl.year}</div>
              <div>Stock: {vinyl.stock}</div>
              <div>Precio: ${vinyl.price}</div>
              <button
                style={{ marginTop: 8 }}
                onClick={() => agregar({ ...vinyl, type: "vinyl", qty: 1 })}
              >
                Agregar al carrito
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Botones simétricos */}
      <div style={{ display: "flex", gap: "1rem", marginTop: "2rem" }}>
        <button style={{ flex: 1 }} onClick={() => setLocalView("cart")}>
          Ver Carrito ({cart.length})
        </button>
        <button style={{ flex: 1 }} onClick={() => setLocalView("upload")}>
          Subir vinilo
        </button>
      </div>
    </div>
  );
}