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