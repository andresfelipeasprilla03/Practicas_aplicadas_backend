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


# ---------- PROVEEDOR ----------
class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id_proveedor = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    nombre_tienda = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Un proveedor puede tener varios vinilos
    vinilos = db.relationship('Vinilo', backref='proveedor', lazy=True)


# ---------- GENERO DE CANCIONES ----------
class Genero(db.Model):
    __tablename__ = 'genero'  # Tabla para los géneros musicales
    id_genero = db.Column(db.Integer, primary_key=True)  # Clave primaria
    nombre = db.Column(db.String(50), nullable=False)  # Nombre del género

    # Un género puede tener muchas canciones
    canciones = db.relationship('Cancion', backref='genero', lazy=True)

# ---------- CANCION ----------
class Cancion(db.Model):
    __tablename__ = 'cancion' # Tabla de canciones
    id_cancion = db.Column(db.Integer, primary_key=True) # Clave primaria
    nombre = db.Column(db.String(100), nullable=False) # Nombre de la canción
    artista = db.Column(db.String(100), nullable=False) # Artista o banda
    duracion_segundos = db.Column(db.Integer) # Duración de la canción en segundos
    tamano_mb = db.Column(db.Numeric(5, 2))  # Tamaño del archivo en MB
    calidad_kbps = db.Column(db.Integer) # Calidad del audio
    precio = db.Column(db.Numeric(6, 2)) # Precio de compra
    id_genero = db.Column(db.Integer, db.ForeignKey('genero.id_genero')) # Género al que pertenece

    # Relaciones con tablas intermedias
    vinilos = db.relationship('CancionVinilo', back_populates='cancion', cascade='all, delete')
    recopilaciones = db.relationship('CancionRecopilacion', back_populates='cancion', cascade='all, delete')

# ---------- VINILO ----------
class Vinilo(db.Model):
    __tablename__ = 'vinilo' # Tabla de vinilos físicos
    id_vinilo = db.Column(db.Integer, primary_key=True)# Clave primaria
    nombre = db.Column(db.String(100), nullable=False)# Nombre del vinilo
    artista = db.Column(db.String(100))# Artista o banda principal
    año_salida = db.Column(db.Date)# Fecha de lanzamiento
    precio = db.Column(db.Numeric(6, 2))# Precio del vinilo
    stock = db.Column(db.Integer)# Cantidad disponible
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id_proveedor'))# Proveedor asociado

    canciones = db.relationship('CancionVinilo', back_populates='vinilo', cascade='all, delete')# Canciones incluidas en este vinilo
    detalles_pedido = db.relationship('DetallePedido', backref='vinilo', lazy=True)# Relación con los detalles de pedidos

# ---------- TABLA INTERMEDIA VINILO - CANCION ----------
class CancionVinilo(db.Model):
    __tablename__ = 'cancion_vinilo'# Tabla intermedia de muchos a muchos
    id_vinilo = db.Column(db.Integer, db.ForeignKey('vinilo.id_vinilo'), primary_key=True)# Vinilo asociado
    id_cancion = db.Column(db.Integer, db.ForeignKey('cancion.id_cancion'), primary_key=True)# Canción asociada

    # Relaciones bidireccionales
    vinilo = db.relationship('Vinilo', back_populates='canciones')
    cancion = db.relationship('Cancion', back_populates='vinilos')

# ---------- PEDIDO ----------
class Pedido(db.Model):
    __tablename__ = 'pedido' # Tabla de pedidos
    id_pedido = db.Column(db.Integer, primary_key=True)# Clave primaria
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow) # Fecha en la que se realizó
    observacion = db.Column(db.Text) # Observaciones del pedido
    fecha_envio = db.Column(db.DateTime) # Fecha propuesta de envío
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario')) # Usuario que hizo el pedido

    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True, cascade='all, delete') # Detalles del pedido (productos)


# ---------- DETALLE DE PEDIDO ----------
class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido' # Tabla de detalle de pedidos
    id_detalle = db.Column(db.Integer, primary_key=True) # Clave primaria
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False) # Pedido asociado
    id_vinilo = db.Column(db.Integer, db.ForeignKey('vinilo.id_vinilo'), nullable=False) # Vinilo asociado
    cantidad = db.Column(db.Integer, nullable=False) # Cantidad comprada
    precio_unitario = db.Column(db.Numeric(8, 2), nullable=False) # Precio por unidad

# ---------- RECOPILACIÓN DE CANCIONES (PLAYLIST) ----------
class Recopilacion(db.Model):
    __tablename__ = 'recopilacion' # Tabla de recopilaciones creadas por usuarios
    id_recopilacion = db.Column(db.Integer, primary_key=True) # Clave primaria
    nombre = db.Column(db.String(100), nullable=False) # Nombre de la playlist
    es_publica = db.Column(db.Boolean, default=False) # Si puede ser vista por otros usuarios
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario')) # Creador de la recopilación

    canciones = db.relationship('CancionRecopilacion', back_populates='recopilacion', cascade='all, delete') # Canciones que contiene

# ---------- TABLA INTERMEDIA RECOPILACIÓN - CANCION ----------
class CancionRecopilacion(db.Model):
    __tablename__ = 'cancion_recopilacion' # Tabla intermedia muchos a muchos
    id_recopilacion = db.Column(db.Integer, db.ForeignKey('recopilacion.id_recopilacion'), primary_key=True) # Recopilación
    id_cancion = db.Column(db.Integer, db.ForeignKey('cancion.id_cancion'), primary_key=True) # Canción

    # Relaciones bidireccionales
    recopilacion = db.relationship('Recopilacion', back_populates='canciones')
    cancion = db.relationship('Cancion', back_populates='recopilaciones')