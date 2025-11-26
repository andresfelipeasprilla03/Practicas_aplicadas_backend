import { useState } from "react";
import App1 from "./App1"; // Importa tu App1
import App2 from "./App2";

function App() {
  const [view, setView] = useState("home"); // "home", "login", "crear", "listar"
  const [usuarios, setUsuarios] = useState([]);
  const [message, setMessage] = useState("");

  // ---------------- Login ----------------
  const [correoLogin, setCorreoLogin] = useState("");
  const [contrasenaLogin, setContrasenaLogin] = useState("");

  const API_URL = "http://127.0.0.1:8000/home/usuarios/";

  const handleLogin = (e) => {
    e.preventDefault();
    fetch(`${API_URL}login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: correoLogin, contrasena: contrasenaLogin }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setMessage("Login exitoso!");
          setView("listar");
        } else {
          setMessage("Usuario o contraseña incorrecta.");
        }
      })
      .catch((err) => {
        console.error(err);
        setMessage("Error en el login.");
      });
  };

  // ---------------- Render ----------------
  if (view === "login") {
    return (
      <div style={{ padding: "2rem" }}>
        <h1>Iniciar Sesión</h1>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Correo"
            value={correoLogin}
            onChange={(e) => setCorreoLogin(e.target.value)}
            required
          />
          <br />
          <input
            type="password"
            placeholder="Contraseña"
            value={contrasenaLogin}
            onChange={(e) => setContrasenaLogin(e.target.value)}
            required
          />
          <br />
          <button type="submit">Iniciar Sesión</button>
        </form>
        <button onClick={() => setView("home")}>Volver</button>
        {message && <p>{message}</p>}
      </div>
    );
  }

  // Cuando view === "crear", renderizamos App1
  if (view === "crear") {
    return <App1 setView={setView} />; // pasamos setView si App1 necesita volver a home o listar
  }

  if (view === "listar") {
    return (
      <div style={{ padding: "2rem" }}>
        <App2 usuarios={usuarios} />
        <button onClick={() => setView("crear")}>Volver a Crear Usuario</button>
      </div>
    );
  }

  // Vista inicial
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Bienvenido</h1>
      <button onClick={() => setView("login")}>Iniciar Sesión</button>
      <button onClick={() => setView("crear")}>Crear Usuario</button>
    </div>
  );
}

export default App;