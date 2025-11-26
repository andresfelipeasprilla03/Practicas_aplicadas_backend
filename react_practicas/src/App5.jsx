import React, { useState } from "react";
import { getVinyl, addToCart } from "../../react_practicas_completed/src/mockApi";
const USER_ID='u1';
export default function App5(props){
  const id = (props && props.id) || (window.location.pathname.split('/').pop());
  const vinyl = getVinyl(id);
  const [qty,setQty] = useState(1);
  function add(){ const res = addToCart(USER_ID,{type:'vinyl',id:vinyl.id,price:vinyl.price,qty}); if(res && res.error) alert(res.error); else alert('Vinilo agregado'); }
  return (
    <div style={{padding:16}}>
      <h2>{vinyl.name}</h2>
      <div>Artista: {vinyl.artist}</div>
      <div>Año: {vinyl.year} • Género: {vinyl.genre}</div>
      <div>Precio: ${vinyl.price} • Stock: {vinyl.stock}</div>
      <label>Cantidad: <input type="number" min="1" max={vinyl.stock} value={qty} onChange={e=>setQty(Number(e.target.value))} /></label>
      <button onClick={add}>Agregar al carrito</button>
      <section>
        <h3>Canciones</h3>
        <ul>{(vinyl.songs||[]).map(sid=> <li key={sid}>{sid}</li>)}</ul>
      </section>
    </div>
  );
}
