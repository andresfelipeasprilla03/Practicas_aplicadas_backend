import React, { useState } from "react";
import { getUser, createCollection, toggleCollectionPrivacy, deleteCollection } from "../../react_practicas_completed/src/mockApi";
const USER_ID='u1';
export default function App7(){
  const user = getUser(USER_ID);
  const [name,setName]=useState('');
  function create(){ if(!name) return alert('Nombre requerido'); createCollection(USER_ID,name,false); setName(''); window.location.reload(); }
  return (
    <div style={{padding:16}}>
      <h2>Recopilaciones</h2>
      <div style={{marginBottom:8}}>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="Nombre" />
        <button onClick={create}>Crear</button>
      </div>
      <div>
        {(user.collections||[]).map(c=>(
          <div key={c.id} style={{border:'1px solid #ddd',padding:8,marginBottom:8,display:'flex',justifyContent:'space-between'}}>
            <div>
              <strong>{c.name}</strong> {c.public ? '(Pública)' : '(Privada)'}
              <div className="small">Canciones: {c.songs.length}</div>
            </div>
            <div>
              <button onClick={()=>{ toggleCollectionPrivacy(USER_ID,c.id); window.location.reload(); }}>Cambiar privacidad</button>
              <button onClick={()=>{ deleteCollection(USER_ID,c.id); window.location.reload(); }}>Eliminar</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
