import React, { useState } from "react";
import { providerCreateVinyl, providerGetOrders, getCatalog } from "../../react_practicas_completed/src/mockApi";
const PROVIDER_ID='p1';
export default function App8(){
  const [name,setName]=useState(''); const [artist,setArtist]=useState(''); const [year,setYear]=useState(2020); const [price,setPrice]=useState(10); const [stock,setStock]=useState(1); const [songsTxt,setSongsTxt]=useState('');
  const orders = providerGetOrders(PROVIDER_ID);
  function create(){ if(!name||!artist) return alert('Nombre y artista oblig'); const songs = songsTxt.split(',').map(s=>s.trim()).filter(Boolean); providerCreateVinyl(PROVIDER_ID,{name,artist,year,price,stock,songs}); alert('Vinilo creado'); window.location.reload(); }
  return (
    <div style={{padding:16}}>
      <h2>Panel de Proveedor</h2>
      <div style={{border:'1px solid #ddd',padding:8,marginBottom:8}}>
        <h3>Crear Vinilo</h3>
        <input placeholder="Nombre" value={name} onChange={e=>setName(e.target.value)} /><br/>
        <input placeholder="Artista" value={artist} onChange={e=>setArtist(e.target.value)} /><br/>
        <input placeholder="Año" type="number" value={year} onChange={e=>setYear(Number(e.target.value))} /><br/>
        <input placeholder="Precio" type="number" value={price} onChange={e=>setPrice(Number(e.target.value))} /><br/>
        <input placeholder="Stock" type="number" value={stock} onChange={e=>setStock(Number(e.target.value))} /><br/>
        <input placeholder="Canciones (separadas por coma)" value={songsTxt} onChange={e=>setSongsTxt(e.target.value)} /><br/>
        <button onClick={create}>Crear</button>
      </div>
      <div>
        <h3>Órdenes</h3>
        {orders.length===0 ? <div>No hay órdenes</div> : orders.map(o=>(
          <div key={o.id} style={{border:'1px solid #ddd',padding:8,marginBottom:8}}>
            <div><strong>Orden:</strong> {o.id} — Estado: {o.status}</div>
            <div>Items: {o.items.length}</div>
            <div>Comprador: {o.buyerId}</div>
            <div><button onClick={()=>{ window.alert('Aceptar orden (simulado)'); }}>Aceptar</button> <button onClick={()=>{ window.alert('Rechazar orden (simulado)'); }}>Rechazar</button></div>
          </div>
        ))}
      </div>
    </div>
  );
}
