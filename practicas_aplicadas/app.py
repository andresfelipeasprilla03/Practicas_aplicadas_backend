# app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from db import db
from models import *
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)  

    # -------- Health --------
    @app.get("/api/health")
    def health():
        return {"ok": True}

    # ====================================================
    # CRUD USUARIO
    # ====================================================
    @app.post("/api/usuarios")
    def create_usuarios():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        data = request.get_json()
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list) or len(data) == 0:
            return jsonify(error="Debe enviar al menos un registro"), 400

        usuarios_creados = []
        for i, item in enumerate(data, start=1):
            nombre = item.get("nombre_completo")
            correo = item.get("correo")
            contrasena = item.get("contrasena")
            if not nombre or not correo or not contrasena:
                return jsonify(error=f"Registro #{i} incompleto"), 400
            u = Usuario(nombre_completo=nombre, correo=correo, contrasena=contrasena)
            usuarios_creados.append(u)
        try:
            db.session.add_all(usuarios_creados)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error=str(e)), 500
        return jsonify([u.id_usuario for u in usuarios_creados]), 201

    @app.get("/api/usuarios")
    def list_usuarios():
        usuarios = Usuario.query.order_by(Usuario.id_usuario.desc()).all()
        return jsonify([u.id_usuario for u in usuarios])

    @app.get("/api/usuarios/<int:id_usuario>")
    def get_usuario(id_usuario):
        u = Usuario.query.get_or_404(id_usuario)
        return jsonify({
            "id_usuario": u.id_usuario,
            "nombre_completo": u.nombre_completo,
            "correo": u.correo
        })

    @app.patch("/api/usuarios/<int:id_usuario>")
    def update_usuario(id_usuario):
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        u = Usuario.query.get_or_404(id_usuario)
        data = request.get_json()
        if "nombre_completo" in data: u.nombre_completo = data["nombre_completo"]
        if "correo" in data: u.correo = data["correo"]
        if "contrasena" in data: u.contrasena = data["contrasena"]
        db.session.commit()
        return jsonify(ok=True)

    @app.delete("/api/usuarios/<int:id_usuario>")
    def delete_usuario(id_usuario):
        u = Usuario.query.get_or_404(id_usuario)
        db.session.delete(u)
        db.session.commit()
        return jsonify(ok=True)

    # ====================================================
    # CRUD PROVEEDOR
    # ====================================================
    @app.post("/api/proveedores")
    def create_proveedor():
        if not request.is_json:
            return jsonify(error="Se requiere JSON"), 415
        data = request.get_json()
        if isinstance(data, dict):
            data = [data]
        proveedores = []
        for item in data:
            nombre_tienda = item.get("nombre_tienda")
            id_usuario = item.get("id_usuario")
            telefono = item.get("telefono")
            if not nombre_tienda or not id_usuario:
                return jsonify(error="Campos obligatorios faltantes"), 400
            p = Proveedor(nombre_tienda=nombre_tienda, telefono=telefono, id_usuario=id_usuario)
            proveedores.append(p)
        try:
            db.session.add_all(proveedores)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify(error=str(e)), 500
        return jsonify(ok=True), 201

    @app.get("/api/proveedores")
    def list_proveedores():
        proveedores = Proveedor.query.all()
        return jsonify([{"id_proveedor": p.id_proveedor, "nombre_tienda": p.nombre_tienda} for p in proveedores])

    @app.delete("/api/proveedores/<int:id_proveedor>")
    def delete_proveedor(id_proveedor):
        p = Proveedor.query.get_or_404(id_proveedor)
        db.session.delete(p)
        db.session.commit()
        return jsonify(ok=True)

    # ====================================================
    # CRUD GENERO
    # ====================================================
    @app.post("/api/generos")
    def create_genero():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        generos = [Genero(nombre=g["nombre"]) for g in data if "nombre" in g]
        db.session.add_all(generos)
        db.session.commit()
        return jsonify(ok=True), 201

    @app.get("/api/generos")
    def list_generos():
        generos = Genero.query.all()
        return jsonify([{"id_genero": g.id_genero, "nombre": g.nombre} for g in generos])

    # ====================================================
    # CRUD CANCION
    # ====================================================
    @app.post("/api/canciones")
    def create_cancion():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        canciones = []
        for c in data:
            canciones.append(Cancion(
                nombre=c.get("nombre"),
                artista=c.get("artista"),
                duracion_segundos=c.get("duracion_segundos"),
                tamano_mb=c.get("tamano_mb"),
                calidad_kbps=c.get("calidad_kbps"),
                precio=c.get("precio"),
                id_genero=c.get("id_genero")
            ))
        db.session.add_all(canciones)
        db.session.commit()
        return jsonify(ok=True), 201

    @app.get("/api/canciones")
    def list_canciones():
        canciones = Cancion.query.all()
        return jsonify([{"id_cancion": c.id_cancion, "nombre": c.nombre, "artista": c.artista} for c in canciones])

    # ====================================================
    # CRUD VINILO
    # ====================================================
    @app.post("/api/vinilos")
    def create_vinilo():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        vinilos = []
        for v in data:
            vinilos.append(Vinilo(
                nombre=v.get("nombre"),
                artista=v.get("artista"),
                año_salida=v.get("año_salida"),
                precio=v.get("precio"),
                stock=v.get("stock"),
                id_proveedor=v.get("id_proveedor")
            ))
        db.session.add_all(vinilos)
        db.session.commit()
        return jsonify(ok=True), 201

    @app.get("/api/vinilos")
    def list_vinilos():
        vinilos = Vinilo.query.all()
        return jsonify([{"id_vinilo": v.id_vinilo, "nombre": v.nombre, "precio": str(v.precio)} for v in vinilos])

    # ====================================================
    # CRUD PEDIDO
    # ====================================================
    @app.post("/api/pedidos")
    def create_pedido():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        pedidos = []
        for p in data:
            pedidos.append(Pedido(
                observacion=p.get("observacion"),
                fecha_envio=p.get("fecha_envio"),
                id_usuario=p.get("id_usuario")
            ))
        db.session.add_all(pedidos)
        db.session.commit()
        return jsonify(ok=True), 201

    @app.get("/api/pedidos")
    def list_pedidos():
        pedidos = Pedido.query.all()
        return jsonify([{"id_pedido": p.id_pedido, "observacion": p.observacion} for p in pedidos])

    # ====================================================
    # CRUD DETALLE_PEDIDO
    # ====================================================
    @app.post("/api/detalle_pedido")
    def create_detalle():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        detalles = []
        for d in data:
            detalles.append(DetallePedido(
                id_pedido=d.get("id_pedido"),
                id_vinilo=d.get("id_vinilo"),
                cantidad=d.get("cantidad"),
                precio_unitario=d.get("precio_unitario")
            ))
        db.session.add_all(detalles)
        db.session.commit()
        return jsonify(ok=True), 201

    @app.get("/api/detalle_pedido")
    def list_detalle():
        detalles = DetallePedido.query.all()
        return jsonify([{
            "id_detalle": d.id_detalle,
            "id_pedido": d.id_pedido,
            "id_vinilo": d.id_vinilo
        } for d in detalles])

    # ====================================================
    # CRUD RECOPILACION
    # ====================================================
    @app.post("/api/recopilaciones")
    def create_recopilacion():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        recs = []
        for r in data:
            recs.append(Recopilacion(nombre=r.get("nombre"), es_publica=r.get("es_publica"), id_usuario=r.get("id_usuario")))
        db.session.add_all(recs)
        db.session.commit()
        return jsonify(ok=True), 201

    @app.get("/api/recopilaciones")
    def list_recopilaciones():
        recs = Recopilacion.query.all()
        return jsonify([{"id_recopilacion": r.id_recopilacion, "nombre": r.nombre} for r in recs])

    # ====================================================
    # CRUD CANCION_VINILO 
    # ====================================================
    @app.post("/api/cancion_vinilo")
    def create_cancion_vinilo():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        enlaces = [CancionVinilo(id_vinilo=i.get("id_vinilo"), id_cancion=i.get("id_cancion")) for i in data]
        db.session.add_all(enlaces)
        db.session.commit()
        return jsonify(ok=True), 201

    # ====================================================
    # CRUD CANCION_RECOPILACION 
    # ====================================================
    @app.post("/api/cancion_recopilacion")
    def create_cancion_recopilacion():
        data = request.get_json()
        if isinstance(data, dict): data = [data]
        enlaces = [CancionRecopilacion(id_recopilacion=i.get("id_recopilacion"), id_cancion=i.get("id_cancion")) for i in data]
        db.session.add_all(enlaces)
        db.session.commit()
        return jsonify(ok=True), 201

    # ← Aquí va el return app correcto
    return app

# Crear instancia de Flask
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)