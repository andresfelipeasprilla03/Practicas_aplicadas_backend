from django.db import models
from django.utils.timezone import now


# ---------------------------
# Usuario
# ---------------------------
class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField(max_length=250, unique=True)
    contrasena = models.CharField(max_length=256)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return self.nombre_completo


# ---------------------------
# Proveedor
# ---------------------------
class Proveedor(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="proveedores")
    nombre_tienda = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    fecha_registro = models.DateTimeField(default=now)

    def __str__(self):
        return self.nombre_tienda


# ---------------------------
# Genero
# ---------------------------
class Genero(models.Model):
    nombre_genero = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_genero


# ---------------------------
# Cancion
# ---------------------------
class Cancion(models.Model):
    nombre_cancion = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    duracion_segundos = models.IntegerField(null=True, blank=True)
    tamano_mb = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calidad_kbps = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, related_name="canciones")

    def __str__(self):
        return f"{self.nombre_cancion} - {self.artista}"


# ---------------------------
# Vinilo
# ---------------------------
class Vinilo(models.Model):
    nombre_vinilo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100, blank=True, null=True)
    año_salida = models.DateField(null=True, blank=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="vinilos")

    def __str__(self):
        return f"{self.nombre_vinilo} - {self.artista or 'Sin artista'} ({self.proveedor})"


# ---------------------------
# CancionVinilo 
# ---------------------------
class CancionVinilo(models.Model):
    vinilo = models.ForeignKey(Vinilo, on_delete=models.CASCADE, related_name="canciones_vinilo")
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="vinilos_cancion")

    class Meta:
        unique_together = ('vinilo', 'cancion')

    def __str__(self):
        return f"{self.cancion} en {self.vinilo}"


# ---------------------------
# Pedido
# ---------------------------
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos")
    fecha_pedido = models.DateTimeField(default=now)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido de {self.usuario} - {self.fecha_pedido.strftime('%Y-%m-%d %H:%M')}"


# ---------------------------
# DetallePedido
# ---------------------------
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    vinilo = models.ForeignKey(Vinilo, on_delete=models.CASCADE, related_name="detalles_pedido")
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.vinilo} para {self.pedido}"


# ---------------------------
# Recopilacion
# ---------------------------
class Recopilacion(models.Model):
    nombre = models.CharField(max_length=100)
    es_publica = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="recopilaciones")

    def __str__(self):
        return f"{self.nombre} ({'Pública' if self.es_publica else 'Privada'})"


# ---------------------------
# CancionRecopilacion 
# ---------------------------
class CancionRecopilacion(models.Model):
    recopilacion = models.ForeignKey(Recopilacion, on_delete=models.CASCADE, related_name="canciones")
    cancion = models.ForeignKey(Cancion, on_delete=models.CASCADE, related_name="recopilaciones")

    class Meta:
        unique_together = ('recopilacion', 'cancion')

    def __str__(self):
        return f"{self.cancion} en {self.recopilacion}"