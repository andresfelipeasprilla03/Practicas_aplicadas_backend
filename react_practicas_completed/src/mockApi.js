// Mock API for react_practicas to provide catalog, songs, vinyls, cart, collections, provider orders.
// Uses localStorage to persist data and is compatible with simple UI components.
const KEY = 'rp:db';

function defaultData(){
  const s1 = {id:'s1', name:'Bohemian Rhapsody', artist:'Queen', price:1.29, duration:'05:55', sizeMb:5.2, kbps:320};
  const s2 = {id:'s2', name:'Another One Bites The Dust', artist:'Queen', price:1.19, duration:'03:35', sizeMb:4.1, kbps:320};
  const v1 = {id:'v1', name:'Greatest Hits', artist:'Queen', year:1981, price:19.99, songs:['s1','s2'], stock:5, genre:'Rock'};
  const users = [{id:'u1', nombre:'Test User', correo:'user@example.com', isProvider:false, purchases:[], favorites:[], collections:[]},
                 {id:'p1', nombre:'Provider Joe', correo:'joe@vinyls.com', isProvider:true, purchases:[], favorites:[], collections:[]}];
  return {songs:[s1,s2], vinyls:[v1], users, carts:{}, orders:[], notifications:[]};
}

function load(){
  const raw = localStorage.getItem(KEY);
  if(!raw){ const d=defaultData(); localStorage.setItem(KEY, JSON.stringify(d)); return d;}
  return JSON.parse(raw);
}
function save(db){ localStorage.setItem(KEY, JSON.stringify(db)); }

export function getCatalog(){ const db=load(); return {songs:db.songs, vinyls:db.vinyls}; }
export function getSong(id){ return load().songs.find(s=>s.id===id); }
export function getVinyl(id){ return load().vinyls.find(v=>v.id===id); }
export function search(q){ const db=load(); const ql=q.toLowerCase(); return {songs:db.songs.filter(s=>s.name.toLowerCase().includes(ql)||s.artist.toLowerCase().includes(ql)), vinyls:db.vinyls.filter(v=>v.name.toLowerCase().includes(ql)||v.artist.toLowerCase().includes(ql)||v.genre.toLowerCase().includes(ql))}; }

export function getCart(userId){ const db=load(); return db.carts[userId] || []; }
export function addToCart(userId,item){
  const db=load(); db.carts[userId]=db.carts[userId]||[];
  if(item.type==='mp3'){
    const u = db.users.find(x=>x.id===userId);
    if(u && u.purchases && u.purchases.includes(item.id)) return {error:'Ya posees esta canción'};
    if(db.carts[userId].some(it=>it.type==='mp3'&&it.id===item.id)) return {error:'Ya en carrito'};
  }
  if(item.type==='vinyl'){
    const v = db.vinyls.find(x=>x.id===item.id);
    if(!v || v.stock<=0) return {error:'Sin stock'};
  }
  db.carts[userId].push(item); save(db); return {ok:true};
}
export function removeFromCart(userId,index){ const db=load(); db.carts[userId]=db.carts[userId]||[]; db.carts[userId].splice(index,1); save(db); }

export function checkout(userId){
  const db=load(); const cart=db.carts[userId]||[]; if(!cart.length) return {error:'Carrito vacío'};
  // validate stock
  for(const it of cart){ if(it.type==='vinyl'){ const v=db.vinyls.find(x=>x.id===it.id); if(!v||v.stock<(it.qty||1)) return {error:'Stock insuficiente'} } }
  const order = {id:'o'+Math.random().toString(36).slice(2,9), buyerId:userId, providerId:'p1', items:cart, status:'creado', createdAt:new Date().toISOString()};
  db.orders.push(order);
  const buyer = db.users.find(u=>u.id===userId);
  for(const it of cart){ if(it.type==='mp3'){ buyer.purchases.push(it.id); } else if(it.type==='vinyl'){ const v=db.vinyls.find(x=>x.id===it.id); v.stock -= (it.qty||1); } }
  db.carts[userId]=[]; db.notifications.push({to:'p1', orderId:order.id, message:'Nuevo pedido', createdAt:new Date().toISOString()});
  save(db);
  return {ok:true, order};
}

export function createCollection(userId, name, isPublic=false){
  const db=load(); const u=db.users.find(x=>x.id===userId); if(!u) return {error:'Usuario no encontrado'};
  const col = {id:'c'+Math.random().toString(36).slice(2,6), name, public:isPublic, songs:[]};
  u.collections.push(col); save(db); return {ok:true, col};
}
export function toggleCollectionPrivacy(userId,colId){ const db=load(); const u=db.users.find(x=>x.id===userId); if(!u) return; const c=u.collections.find(x=>x.id===colId); if(c) c.public=!c.public; save(db); }
export function deleteCollection(userId,colId){ const db=load(); const u=db.users.find(x=>x.id===userId); if(!u) return; u.collections=u.collections.filter(x=>x.id!==colId); save(db); }

export function toggleFavorite(userId,itemId){ const db=load(); const u=db.users.find(x=>x.id===userId); if(!u) return; u.favorites=u.favorites||[]; const idx=u.favorites.indexOf(itemId); if(idx>=0) u.favorites.splice(idx,1); else u.favorites.push(itemId); save(db); }
export function getUser(userId){ return load().users.find(u=>u.id===userId); }

export function providerCreateVinyl(providerId, vinyl){
  const db=load(); vinyl.id='v'+Math.random().toString(36).slice(2,8); db.vinyls.push(vinyl); save(db); return {ok:true, vinyl};
}
export function providerGetOrders(providerId){ return load().orders.filter(o=>o.providerId===providerId); }
export function providerSetOrderStatus(orderId,status){ const db=load(); const o=db.orders.find(x=>x.id===orderId); if(!o) return {error:'Orden no encontrada'}; o.status=status; save(db); return {ok:true}; }

export function debug(){ return load(); }
