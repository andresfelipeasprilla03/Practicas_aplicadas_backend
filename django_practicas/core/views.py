# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import (
    Usuario, Proveedor, Genero, Cancion, Vinilo, Pedido,
    DetallePedido, Recopilacion, CancionVinilo, CancionRecopilacion
)
from .forms import (
    UsuarioForm, ProveedorForm, GeneroForm, CancionForm, ViniloForm,
    PedidoForm, DetallePedidoForm, RecopilacionForm,
    CancionViniloForm, CancionRecopilacionForm
)


# ====================== BÁSICOS ======================
def home(request):
    return render(request, "home.html", {"title": "Tienda de Vinilos y Música Digital"})


def api_ping(request):
    return JsonResponse({"ok": True, "message": "pong"})


def api_echo(request):
    msg = request.GET.get("msg")
    if not msg:
        return JsonResponse({"error": "Falta 'msg'."}, status=400)
    return JsonResponse({"echo": msg, "length": len(msg)})


# ====================== USUARIO ======================
def usuario_list(request):
    qs = Usuario.objects.all().order_by('-id')
    return render(request, "usuario/list.html", {"object_list": qs})


@require_http_methods(["GET", "POST"])
def usuario_create(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:usuario_list")
    else:
        form = UsuarioForm()
    return render(request, "usuario/form.html", {"form": form, "mode": "create"})


@require_http_methods(["GET", "POST"])
def usuario_update(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("core:usuario_list")
    else:
        form = UsuarioForm(instance=obj)
    return render(request, "usuario/form.html", {"form": form, "mode": "edit", "object": obj})


@require_http_methods(["GET", "POST"])
def usuario_delete(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("core:usuario_list")
    return render(request, "usuario/confirm_delete.html", {"object": obj})


# ====================== PROVEEDOR ======================
def proveedor_list(request):
    qs = Proveedor.objects.select_related("usuario").all()
    return render(request, "proveedor/list.html", {"object_list": qs})

@require_http_methods(["GET", "POST"])
def proveedor_create(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:proveedor_list")
    else:
        form = ProveedorForm()
    return render(request, "proveedor/form.html", {"form": form, "mode": "create"})

@require_http_methods(["GET", "POST"])
def proveedor_update(request, pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("core:proveedor_list")
    else:
        form = ProveedorForm(instance=obj)
    return render(request, "proveedor/form.html", {"form": form, "mode": "edit", "object": obj})

@require_http_methods(["GET", "POST"])
def proveedor_delete(request, pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("core:proveedor_list")
    return render(request, "proveedor/confirm_delete.html", {"object": obj})


# ====================== GÉNERO ======================
def genero_list(request):
    qs = Genero.objects.all()
    return render(request, "genero/list.html", {"object_list": qs})

@require_http_methods(["GET", "POST"])
def genero_create(request):
    if request.method == "POST":
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:genero_list")
    else:
        form = GeneroForm()
    return render(request, "genero/form.html", {"form": form, "mode": "create"})


# ====================== VINILO ======================
def vinilo_list(request):
    qs = Vinilo.objects.select_related("proveedor__usuario").all()
    return render(request, "vinilo/list.html", {"object_list": qs})

@require_http_methods(["GET", "POST"])
def vinilo_create(request):
    if request.method == "POST":
        form = ViniloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:vinilo_list")
    else:
        form = ViniloForm()
    return render(request, "vinilo/form.html", {"form": form, "mode": "create"})


# ====================== CANCIÓN ======================
def cancion_list(request):
    qs = Cancion.objects.select_related("genero").all()
    return render(request, "cancion/list.html", {"object_list": qs})

@require_http_methods(["GET", "POST"])
def cancion_create(request):
    if request.method == "POST":
        form = CancionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:cancion_list")
    else:
        form = CancionForm()
    return render(request, "cancion/form.html", {"form": form, "mode": "create"})


# ====================== PEDIDO ======================
def pedido_list(request):
    qs = Pedido.objects.select_related("usuario").all()
    return render(request, "pedido/list.html", {"object_list": qs})


# ====================== RECOPILACIÓN ======================
def recopilacion_list(request):
    qs = Recopilacion.objects.select_related("usuario").all()
    return render(request, "recopilacion/list.html", {"object_list": qs})