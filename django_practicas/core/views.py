from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import *
from .forms import *
# ====================== BÁSICOS ======================
def home(request):
    return JsonResponse({"title": "Tienda de Vinilos y Música Digital"})


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
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)


@require_http_methods(["GET", "POST"])
def usuario_create(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = UsuarioForm()
    return JsonResponse({"form": "GET request - form not serialized", "mode": "create"})


@require_http_methods(["GET", "POST"])
def usuario_update(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = UsuarioForm(instance=obj)
    return JsonResponse({"form": "GET request - form not serialized", "mode": "edit", "object": serialize("json", [obj])})


@require_http_methods(["GET", "POST"])
def usuario_delete(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    if request.method == "POST":
        obj.delete()
        return JsonResponse({"deleted": True})
    return JsonResponse({"object": serialize("json", [obj])})


# ====================== PROVEEDOR ======================
def proveedor_list(request):
    qs = Proveedor.objects.select_related("usuario").all()
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)


@require_http_methods(["GET", "POST"])
def proveedor_create(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = ProveedorForm()
    return JsonResponse({"form": "GET request - form not serialized", "mode": "create"})


@require_http_methods(["GET", "POST"])
def proveedor_update(request, pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = ProveedorForm(instance=obj)
    return JsonResponse({"form": "GET request - form not serialized", "mode": "edit", "object": serialize("json", [obj])})


@require_http_methods(["GET", "POST"])
def proveedor_delete(request, pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        obj.delete()
        return JsonResponse({"deleted": True})
    return JsonResponse({"object": serialize("json", [obj])})


# ====================== GÉNERO ======================
def genero_list(request):
    qs = Genero.objects.all()
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)


@require_http_methods(["GET", "POST"])
def genero_create(request):
    if request.method == "POST":
        form = GeneroForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = GeneroForm()
    return JsonResponse({"form": "GET request - form not serialized", "mode": "create"})


# ====================== VINILO ======================
def vinilo_list(request):
    qs = Vinilo.objects.select_related("proveedor__usuario").all()
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)


@require_http_methods(["GET", "POST"])
def vinilo_create(request):
    if request.method == "POST":
        form = ViniloForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = ViniloForm()
    return JsonResponse({"form": "GET request - form not serialized", "mode": "create"})


# ====================== CANCIÓN ======================
def cancion_list(request):
    qs = Cancion.objects.select_related("genero").all()
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)


@require_http_methods(["GET", "POST"])
def cancion_create(request):
    if request.method == "POST":
        form = CancionForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({"object": serialize("json", [obj])}, safe=False)
    else:
        form = CancionForm()
    return JsonResponse({"form": "GET request - form not serialized", "mode": "create"})


# ====================== PEDIDO ======================
def pedido_list(request):
    qs = Pedido.objects.select_related("usuario").all()
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)


# ====================== RECOPILACIÓN ======================
def recopilacion_list(request):
    qs = Recopilacion.objects.select_related("usuario").all()
    return JsonResponse({"object_list": serialize("json", qs)}, safe=False)
