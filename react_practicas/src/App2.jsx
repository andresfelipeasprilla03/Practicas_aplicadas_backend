import { useState, useEffect } from "react";

function App2() {
  const [usuarios, setUsuarios] = useState([]);
  const [message, setMessage] = useState("");

  const API_URL = "http://127.0.0.1:8000/home/usuarios/";

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => {
        let lista = data.object_list;
        if (typeof lista === "string") lista = JSON.parse(lista);
        setUsuarios(lista);
      })
      .catch((err) => {
        console.error(err);
        setMessage("Error al cargar usuarios.");
      });
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Usuarios Registrados</h1>

      {message && <p>{message}</p>}

      <ul>
        {usuarios.map((u) => (
          <li key={u.pk}>
            <strong>Nombre:</strong> {u.fields.nombre_completo} <br />
            <strong>Correo:</strong> {u.fields.correo} <br />
            <strong>Fecha de registro:</strong> {u.fields.fecha_registro}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App2;