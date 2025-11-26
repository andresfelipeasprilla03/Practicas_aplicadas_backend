from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/ping/", views.api_ping, name="api_ping"),
    path("api/echo/", views.api_echo, name="api_echo"),

    # Usuario
    path("usuarios/", views.usuario_list, name="usuario_list"),
    path("usuarios/new/", views.usuario_create, name="usuario_create"),
    path("usuarios/<int:pk>/edit/", views.usuario_update, name="usuario_update"),
    path("usuarios/<int:pk>/delete/", views.usuario_delete, name="usuario_delete"),
    path("usuarios/login/", views.usuario_login, name="usuario_login"),

    # Proveedor
    path("proveedores/", views.proveedor_list, name="proveedor_list"),
    path("proveedores/new/", views.proveedor_create, name="proveedor_create"),
    path("proveedores/<int:pk>/edit/", views.proveedor_update, name="proveedor_update"),
    path("proveedores/<int:pk>/delete/", views.proveedor_delete, name="proveedor_delete"),

    # Género
    path("generos/", views.genero_list, name="genero_list"),
    path("generos/new/", views.genero_create, name="genero_create"),

    # Vinilo
    path("vinilos/", views.vinilo_list, name="vinilo_list"),
    path("vinilos/new/", views.vinilo_create, name="vinilo_create"),

    # Canción
    path("canciones/", views.cancion_list, name="cancion_list"),
    path("canciones/new/", views.cancion_create, name="cancion_create"),

    # Pedido y Recopilación
    path("pedidos/", views.pedido_list, name="pedido_list"),
    path("recopilaciones/", views.recopilacion_list, name="recopilacion_list"),
]
