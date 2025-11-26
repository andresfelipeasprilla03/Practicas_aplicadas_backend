from django import forms
from .models import *


# ---------------------------
# Usuario
# ---------------------------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'contrasena': forms.PasswordInput(),  # ocultar contraseña
        }


# ---------------------------
# Proveedor
# ---------------------------
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'


# ---------------------------
# Género
# ---------------------------
class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = '__all__'


# ---------------------------
# Canción
# ---------------------------
class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = '__all__'


# ---------------------------
# Vinilo
# ---------------------------
class ViniloForm(forms.ModelForm):
    class Meta:
        model = Vinilo
        fields = '__all__'


# ---------------------------
# CancionVinilo (tabla puente)
# ---------------------------
class CancionViniloForm(forms.ModelForm):
    class Meta:
        model = CancionVinilo
        fields = '__all__'


# ---------------------------
# Pedido
# ---------------------------
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'


# ---------------------------
# DetallePedido
# ---------------------------
class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '__all__'


# ---------------------------
# Recopilación
# ---------------------------
class RecopilacionForm(forms.ModelForm):
    class Meta:
        model = Recopilacion
        fields = '__all__'


# ---------------------------
# CancionRecopilacion (tabla puente)
# ---------------------------
class CancionRecopilacionForm(forms.ModelForm):
    class Meta:
        model = CancionRecopilacion
        fields = '__all__'

        # ---------------------------
# Carrito
# ---------------------------
class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = '__all__'

# ---------------------------
# CarritoItem
# ---------------------------
class CarritoItemForm(forms.ModelForm):
    class Meta:
        model = CarritoItem
        fields = '__all__'