import React, { useState } from "react";

function CrearUsuario() {
  const [nombre, setNombre] = useState("");
  const [correo, setCorreo] = useState("");
  const [contrasena, setContrasena] = useState("");
   const [fecha_registro, setfecha_registro] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); // Evita que la página se recargue

    // Creamos el objeto a enviar
    const usuarioData = {
      nombre_completo: nombre,
      correo: correo,
      contrasena: contrasena,
      fecha_registro,fecha_registro,
    };

    fetch("http://127.0.0.1:8000/home/usuarios/new/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(usuarioData),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Usuario creado:", data);
        // Limpiar el formulario
        setNombre("");
        setCorreo("");
        setContrasena("");
        setfecha_registro("");
      })
      .catch((err) => console.error("Error creando usuario:", err));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Nombre completo"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <input
        type="email"
        placeholder="Correo"
        value={correo}
        onChange={(e) => setCorreo(e.target.value)}
      />
      <input
        type="text"
        placeholder="Contraseña"
        value={contrasena}
        onChange={(e) => setContrasena(e.target.value)}
      />
      <input
        type="date"
        placeholder="fecha_registro"
        value={fecha_registro}
        onChange={(e) => setfecha_registro(e.target.value)}
      />
      <button type="submit">Crear Usuario</button>
    </form>
  );
}

export default CrearUsuario;