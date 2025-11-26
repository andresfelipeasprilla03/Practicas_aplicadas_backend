import { useState } from "react";

function App1({ setView }) {
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [fechaRegistro, setFechaRegistro] = useState("");
  const [message, setMessage] = useState("");

  const API_URL = "http://127.0.0.1:8000/home/usuarios/";

  const handleSubmit = (e) => {
    e.preventDefault();

    const nuevoUsuario = {
      nombre_completo: nombre,
      correo: correo,
      contrasena: contrasena,
      fecha_registro: fechaRegistro,
    };

    fetch(`${API_URL}new/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nuevoUsuario),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.errors) {
          setMessage(
            "Error: " +
              Object.entries(data.errors)
                .map(([k, v]) => `${k}: ${v}`)
                .join(", ")
          );
        } else {
          setMessage("Usuario creado correctamente!");
          setNombre("");
          setCorreo("");
          setContrasena("");
          setFechaRegistro("");

          // 🔹 Cambio de vista a login automáticamente
          setView("login");
        }
      })
      .catch((err) => {
        console.error(err);
        setMessage("Error al crear el usuario.");
      });
  };

 return (
  <div style={{ padding: "2rem", textAlign: "center" }}>
    <h1>Crear Usuario</h1>
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1rem" }}>
      <input
        type="text"
        placeholder="Nombre completo"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="Correo"
        value={correo}
        onChange={(e) => setCorreo(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Contraseña"
        value={contrasena}
        onChange={(e) => setContrasena(e.target.value)}
        required
      />
      <input
        type="date"
        placeholder="Fecha de registro"
        value={fechaRegistro}
        onChange={(e) => setFechaRegistro(e.target.value)}
        required
      />
      <div style={{ display: "flex", justifyContent: "center", gap: "1rem" }}>
        <button type="submit">Crear Usuario</button>
        <button type="button" onClick={() => setView("home")}>Volver</button>
      </div>
    </form>

    {message && <p>{message}</p>}
  </div>
);
}

export default App1;