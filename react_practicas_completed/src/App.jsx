import { useState } from "react";
import App1 from "./App1"; // Formulario para crear usuario
import App2 from "./App2"; // Lista de usuarios

function App() {
  const [view, setView] = useState("home"); // "home", "crear", "login", "listar"
  const [usuarios, setUsuarios] = useState([]);
  const [message, setMessage] = useState("");

  // Datos login
  const [correoLogin, setCorreoLogin] = useState("");
  const [contrasenaLogin, setContrasenaLogin] = useState("");
  const [usuarioActual, setUsuarioActual] = useState(null);

  const API_URL = "http://127.0.0.1:8000/home/usuarios/";

  // ---------------- Login ----------------
  const handleLogin = (e) => {
    e.preventDefault();
    setMessage("");

    fetch(`${API_URL}login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: correoLogin, contrasena: contrasenaLogin }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setUsuarioActual(data.usuario);
          setMessage("Login exitoso!");
          setView("listar"); // Mostrar lista después de login
        } else {
          setMessage(data.message || "Correo o contraseña incorrecta.");
        }
      })
      .catch((err) => {
        console.error(err);
        setMessage("Error al conectar con el servidor.");
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

  if (view === "crear") {
    return <App1 setView={setView} />; // Vista de crear usuario
  }

  if (view === "listar") {
    return (
      <div style={{ padding: "2rem" }}>
        <h2>Bienvenido, {usuarioActual?.nombre_completo}</h2>
        <App2 usuarios={usuarios} />
        <button onClick={() => setView("home")}>Cerrar sesión</button>
      </div>
    );
  }

  // Vista inicial (home)
  return (
    <div style={{ padding: "2rem" }}>
      <h1>Bienvenido</h1>
      <button onClick={() => setView("login")}>Iniciar Sesión</button>
      <button onClick={() => setView("crear")}>Crear Usuario</button>
    </div>
  );
}

export default App;