import React from "react";
import { getCart, removeFromCart, checkout, getCatalog } from "../../react_practicas_completed/src/mockApi";
const USER_ID='u1';
export default function App6(){
  const cart = getCart(USER_ID);
  const catalog = getCatalog();
  function remove(i){ removeFromCart(USER_ID,i); window.location.reload(); }
  function doCheckout(){ const res = checkout(USER_ID); if(res && res.error) alert(res.error); else alert('Orden creada: '+res.order.id); window.location.reload(); }
  return (
    <div style={{padding:16}}>
      <h2>Carrito</h2>
      {cart.length===0 ? <div>Carrito vacío</div> : (
        <div>
          {cart.map((it,idx)=>(
            <div key={idx} style={{border:'1px solid #ddd',padding:8,marginBottom:8,display:'flex',justifyContent:'space-between'}}>
              <div>
                <div><strong>{it.type==='mp3' ? (catalog.songs.find(s=>s.id===it.id)||{}).name : (catalog.vinyls.find(v=>v.id===it.id)||{}).name}</strong></div>
                <div className="small">{it.type}</div>
              </div>
              <div>
                <div>Precio: ${it.price} {it.qty ? ' x '+it.qty : ''}</div>
                <button onClick={()=>remove(idx)}>Eliminar</button>
              </div>
            </div>
          ))}
          <button onClick={doCheckout}>Finalizar compra (simulado)</button>
        </div>
      )}
    </div>
  );
}
