from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------------------
# MODELOS PRINCIPALES
# ---------------------------

# ---------- USUARIO ----------
class Usuario(db.Model):
    __tablename__ = 'usuario'  # Nombre de la tabla en la base de datos
    id_usuario = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre_completo = db.Column(db.String(100), nullable=False)  # Nombre completo del usuario
    correo = db.Column(db.String(250), unique=True, nullable=False)  # Correo único
    contrasena = db.Column(db.String(256), nullable=False)  # Contraseña encriptada
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de registro automática

    # Relaciones: un usuario puede tener varios pedidos, proveedores y recopilaciones
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)
    proveedores = db.relationship('Proveedor', backref='usuario', lazy=True)
    recopilaciones = db.relationship('Recopilacion', backref='usuario', lazy=True)


class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    nombre_tienda = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    vinilos = db.relationship('Vinilo', backref='proveedor', lazy=True)


class Genero(db.Model):
    __tablename__ = 'genero'
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    canciones = db.relationship('Cancion', backref='genero', lazy=True)


class Cancion(db.Model):
    __tablename__ = 'cancion'
    id_cancion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100), nullable=False)
    duracion_segundos = db.Column(db.Integer)
    tamano_mb = db.Column(db.Numeric(5, 2))
    calidad_kbps = db.Column(db.Integer)
    precio = db.Column(db.Numeric(6, 2))
    id_genero = db.Column(db.Integer, db.ForeignKey('genero.id_genero'))

    vinilos = db.relationship('CancionVinilo', back_populates='cancion', cascade='all, delete')
    recopilaciones = db.relationship('CancionRecopilacion', back_populates='cancion', cascade='all, delete')


class Vinilo(db.Model):
    __tablename__ = 'vinilo'
    id_vinilo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    artista = db.Column(db.String(100))
    año_salida = db.Column(db.Date)
    precio = db.Column(db.Numeric(6, 2))
    stock = db.Column(db.Integer)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id_proveedor'))

    canciones = db.relationship('CancionVinilo', back_populates='vinilo', cascade='all, delete')
    detalles_pedido = db.relationship('DetallePedido', backref='vinilo', lazy=True)


class CancionVinilo(db.Model):
    __tablename__ = 'cancion_vinilo'
    id_vinilo = db.Column(db.Integer, db.ForeignKey('vinilo.id_vinilo'), primary_key=True)
    id_cancion = db.Column(db.Integer, db.ForeignKey('cancion.id_cancion'), primary_key=True)

    vinilo = db.relationship('Vinilo', back_populates='canciones')
    cancion = db.relationship('Cancion', back_populates='vinilos')


class Pedido(db.Model):
    __tablename__ = 'pedido'
    id_pedido = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)
    observacion = db.Column(db.Text)
    fecha_envio = db.Column(db.DateTime)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True, cascade='all, delete')


class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False)
    id_vinilo = db.Column(db.Integer, db.ForeignKey('vinilo.id_vinilo'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(8, 2), nullable=False)


class Recopilacion(db.Model):
    __tablename__ = 'recopilacion'
    id_recopilacion = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    es_publica = db.Column(db.Boolean, default=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

    canciones = db.relationship('CancionRecopilacion', back_populates='recopilacion', cascade='all, delete')


class CancionRecopilacion(db.Model):
    __tablename__ = 'cancion_recopilacion'
    id_recopilacion = db.Column(db.Integer, db.ForeignKey('recopilacion.id_recopilacion'), primary_key=True)
    id_cancion = db.Column(db.Integer, db.ForeignKey('cancion.id_cancion'), primary_key=True)

    recopilacion = db.relationship('Recopilacion', back_populates='canciones')
    cancion = db.relationship('Cancion', back_populates='recopilaciones')