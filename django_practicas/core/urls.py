from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # --------------------------- BASICOS ---------------------------
    path("", views.home, name="home"),
    path("api/ping/", views.api_ping, name="api_ping"),
    path("api/echo/", views.api_echo, name="api_echo"),

    # --------------------------- USUARIO ---------------------------
    path("usuarios/", views.usuario_list, name="usuario_list"),
    path("usuarios/new/", views.usuario_create, name="usuario_create"),
    path("usuarios/<int:pk>/edit/", views.usuario_update, name="usuario_update"),
    path("usuarios/<int:pk>/delete/", views.usuario_delete, name="usuario_delete"),
    path("usuarios/login/", views.usuario_login, name="usuario_login"),

    # --------------------------- PROVEEDOR --------------------------
    path("proveedores/", views.proveedor_list, name="proveedor_list"),
    path("proveedores/new/", views.proveedor_create, name="proveedor_create"),
    path("proveedores/<int:pk>/edit/", views.proveedor_update, name="proveedor_update"),
    path("proveedores/<int:pk>/delete/", views.proveedor_delete, name="proveedor_delete"),

    # --------------------------- GÉNERO ----------------------------
    path("generos/", views.genero_list, name="genero_list"),
    path("generos/new/", views.genero_create, name="genero_create"),

    # --------------------------- VINILO ----------------------------
    path("vinilos/", views.vinilo_list, name="vinilo_list"),
    path("vinilos/new/", views.vinilo_create, name="vinilo_create"),
    path("vinilos/<int:pk>/edit/", views.vinilo_update, name="vinilo_update"),
    path("vinilos/<int:pk>/delete/", views.vinilo_delete, name="vinilo_delete"),

    # --------------------------- CANCIÓN --------------------------
    path("canciones/", views.cancion_list, name="cancion_list"),
    path("canciones/new/", views.cancion_create, name="cancion_create"),

    # --------------------------- PEDIDO ----------------------------
    path("pedidos/", views.pedido_list, name="pedido_list"),
    path("pedidos/new/", views.pedido_create, name="pedido_create"),
    path("pedidos/<int:pk>/edit/", views.pedido_update, name="pedido_update"),
    path("pedidos/<int:pk>/delete/", views.pedido_delete, name="pedido_delete"),

    # --------------------------- RECOPILACIÓN ----------------------
    path("recopilaciones/", views.recopilacion_list, name="recopilacion_list"),
    path("recopilaciones/new/", views.recopilacion_create, name="recopilacion_create"),
    path("recopilaciones/<int:pk>/edit/", views.recopilacion_update, name="recopilacion_update"),
    path("recopilaciones/<int:pk>/delete/", views.recopilacion_delete, name="recopilacion_delete"),

     # --------------------- CARRITO ---------------------
    path('carritos/', views.carrito_list, name='carrito_list'),
    path('carritos/nuevo/', views.carrito_create, name='carrito_create'),
    path('carritos/<int:pk>/editar/', views.carrito_update, name='carrito_update'),
    path('carritos/<int:pk>/eliminar/', views.carrito_delete, name='carrito_delete'),

    # --------------------- CARRITO ITEM ---------------------
    path('carrito-items/', views.carritoitem_list, name='carritoitem_list'),
    path('carrito-items/nuevo/', views.carritoitem_create, name='carritoitem_create'),
    path('carrito-items/<int:pk>/editar/', views.carritoitem_update, name='carritoitem_update'),
    path('carrito-items/<int:pk>/eliminar/', views.carritoitem_delete, name='carritoitem_delete'),
]