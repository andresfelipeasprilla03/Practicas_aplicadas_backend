from django import forms
from .models import (
    Category,
    Product,
    Usuario,
    Proveedor,
    Genero,
    Cancion,
    Vinilo,
    CancionVinilo,
    Pedido,
    DetallePedido,
    Recopilacion,
    CancionRecopilacion,
)


# ---------------------------
# Categoría y Producto
# ---------------------------
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '_all_'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '_all_'


# ---------------------------
# Usuario
# ---------------------------
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '_all_'
        widgets = {
            'contrasena': forms.PasswordInput(),  # ocultar contraseña
        }


# ---------------------------
# Proveedor
# ---------------------------
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '_all_'


# ---------------------------
# Género
# ---------------------------
class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = '_all_'


# ---------------------------
# Canción
# ---------------------------
class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = '_all_'


# ---------------------------
# Vinilo
# ---------------------------
class ViniloForm(forms.ModelForm):
    class Meta:
        model = Vinilo
        fields = '_all_'


# ---------------------------
# CancionVinilo (tabla puente)
# ---------------------------
class CancionViniloForm(forms.ModelForm):
    class Meta:
        model = CancionVinilo
        fields = '_all_'


# ---------------------------
# Pedido
# ---------------------------
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '_all_'


# ---------------------------
# DetallePedido
# ---------------------------
class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = '_all_'


# ---------------------------
# Recopilación
# ---------------------------
class RecopilacionForm(forms.ModelForm):
    class Meta:
        model = Recopilacion
        fields = '_all_'


# ---------------------------
# CancionRecopilacion (tabla puente)
# ---------------------------
class CancionRecopilacionForm(forms.ModelForm):
    class Meta:
        model = CancionRecopilacion
        fields = '_all_'