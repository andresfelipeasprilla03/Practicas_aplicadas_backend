import { useState, useEffect } from "react";

function App() {
  const [usuarios, setUsuarios] = useState([]);
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [message, setMessage] = useState("");

  const API_URL = "http://127.0.0.1:8000/home/usuarios/";

  // ---------------- Listar usuarios ----------------
  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        // Si tu JSON viene con "object_list" serializado como string
        let lista = data.object_list;
        if (typeof lista === "string") lista = JSON.parse(lista);
        setUsuarios(lista);
      })
      .catch((err) => console.error(err));
  }, []);

  // ---------------- Crear usuario ----------------
  const handleSubmit = (e) => {
    e.preventDefault();

    const nuevoUsuario = {
      nombre_completo: nombre,
      correo: correo,
      contrasena: contrasena,
    };

    // Convertimos a x-www-form-urlencoded para Django Form
    const bodyData = new URLSearchParams(nuevoUsuario);

    fetch(`${API_URL}new/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: bodyData,
    })
      .then((res) => res.json())
      .then((data) => {
        let obj = data.object;
        if (typeof obj === "string") obj = JSON.parse(obj)[0]; // tomar primer objeto
        setUsuarios((prev) => [...prev, obj]);
        setMessage("Usuario creado correctamente!");
        setNombre("");
        setCorreo("");
        setContrasena("");
      })
      .catch((err) => {
        console.error(err);
        setMessage("Error al crear el usuario.");
      });
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Usuarios</h1>

      <ul>
        {usuarios.map((u) => (
          <li key={u.pk}>
            {u.fields.nombre_completo} - {u.fields.correo}
          </li>
        ))}
      </ul>

      <h2>Crear Usuario</h2>
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
         <br />
        <input
          type="date"
          placeholder="Contraseña"
          value={contrasena}
          onChange={(e) => setContrasena(e.target.value)}
          required
        />
        <br />
        <button type="submit">Crear Usuario</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default App;