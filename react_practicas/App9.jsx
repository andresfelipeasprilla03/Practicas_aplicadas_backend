import React from "react";
import { getCatalog, providerGetOrders } from "../react_practicas_completed/src/mockApi";
export default function App9(){
  const catalog = getCatalog();
  const orders = providerGetOrders('p1');
  return (
    <div style={{padding:16}}>
      <h2>Panel Admin</h2>
      <section>
        <h3>Consistencia de catálogo</h3>
        <div>Vinilos totales: {catalog.vinyls.length} — Canciones totales: {catalog.songs.length}</div>
      </section>
      <section style={{marginTop:12}}>
        <h3>Órdenes (todos)</h3>
        {orders.map(o=>(
          <div key={o.id} style={{border:'1px solid #ddd',padding:8,marginBottom:8}}>
            <div>ID: {o.id} — Estado: {o.status}</div>
            <div>Items: {o.items.length}</div>
          </div>
        ))}
      </section>
    </div>
  );
}
