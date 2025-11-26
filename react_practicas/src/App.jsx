import { useState } from "react";
import App2 from "./App2";

function App() {
  const [view, setView] = useState("crear"); // "crear" o "listar"
  const [usuarios, setUsuarios] = useState([]);
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [fechaRegistro, setFechaRegistro] = useState("");
  const [message, setMessage] = useState("");

  const API_URL = "http://127.0.0.1:8000/home/usuarios/";

  // ---------------- Crear usuario ----------------
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
      headers: {
        "Content-Type": "application/json",
      },
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
          let obj = data.object;
          if (typeof obj === "string") obj = JSON.parse(obj)[0];
          setUsuarios((prev) => [...prev, obj]);
          setMessage("Usuario creado correctamente!");
          setNombre("");
          setCorreo("");
          setContrasena("");
          setFechaRegistro("");
        }
      })
      .catch((err) => {
        console.error(err);
        setMessage("Error al crear el usuario.");
      });
  };

  // ---------------- Render ----------------
  if (view === "listar") {
    return (
      <div style={{ padding: "2rem" }}>
        <App2 usuarios={usuarios} />
         <button onClick={() => setView("crear")}>Volver a Crear Usuario</button>
      </div>
    );
  }

  // Vista crear usuario
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Crear Usuario</h1>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nombre completo"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />
        <br />
        <input
          type="email"
          placeholder="Correo"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
        />
        <br />
        <input
          type="password"
          placeholder="Contraseña"
          value={contrasena}
          onChange={(e) => setContrasena(e.target.value)}
          required
        />
        <br />
        <input
          type="date"
          placeholder="Fecha de registro"
          value={fechaRegistro}
          onChange={(e) => setFechaRegistro(e.target.value)}
          required
        />
        <br />
        <button type="submit">Crear Usuario</button>
        <button onClick={() => setView("listar")}>Ver Usuarios</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default App;