from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from .models import *
from .forms import *
import json
from django.forms.models import model_to_dict

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
@csrf_exempt
@require_http_methods(["POST"])
def usuario_create(request):
    """Crea un usuario con contraseña en texto plano"""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    form = UsuarioForm(data)
    if form.is_valid():
        obj = form.save()  # contraseña en texto plano
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)


def usuario_list(request):
    qs = Usuario.objects.all().order_by('-id')
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def usuario_update(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    form = UsuarioForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def usuario_delete(request, pk):
    obj = get_object_or_404(Usuario, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})


@csrf_exempt
@require_http_methods(["POST"])
def usuario_login(request):
    """Login de usuario, contraseña en texto plano"""
    try:
        data = json.loads(request.body)
        correo = data.get("correo", "").strip()
        contrasena = data.get("contrasena", "").strip()
        usuario = Usuario.objects.filter(correo=correo, contrasena=contrasena).first()
        if usuario:
            return JsonResponse({
                "success": True,
                "usuario": {
                    "id": usuario.id,
                    "nombre_completo": usuario.nombre_completo,
                    "correo": usuario.correo
                }
            })
        return JsonResponse({"success": False, "message": "Correo o contraseña incorrecta."})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})
    
    # ====================== PROVEEDOR ======================
def proveedor_list(request):
    qs = Proveedor.objects.select_related("usuario").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def proveedor_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = ProveedorForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def proveedor_update(request, pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = ProveedorForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def proveedor_delete(request, pk):
    obj = get_object_or_404(Proveedor, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})


# ====================== GÉNERO ======================
def genero_list(request):
    qs = Genero.objects.all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def genero_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = GeneroForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)


# ====================== VINILO ======================
def vinilo_list(request):
    qs = Vinilo.objects.select_related("proveedor__usuario").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def vinilo_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = ViniloForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def vinilo_update(request, pk):
    obj = get_object_or_404(Vinilo, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = ViniloForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def vinilo_delete(request, pk):
    obj = get_object_or_404(Vinilo, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})


# ====================== CANCIÓN ======================
def cancion_list(request):
    qs = Cancion.objects.select_related("genero").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def cancion_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    genero_id = data.get("genero")
    if genero_id:
        try:
            data["genero"] = Genero.objects.get(pk=genero_id).id
        except Genero.DoesNotExist:
            return JsonResponse({"error": "Genero no existe"}, status=400)

    form = CancionForm(data)
    if form.is_valid():
        obj = form.save()
        obj_dict = model_to_dict(obj)
        obj_dict["genero"] = obj.genero.id if obj.genero else None
        return JsonResponse({"object": obj_dict}, status=201)
    return JsonResponse({"errors": form.errors}, status=400)


# ====================== PEDIDO ======================
def pedido_list(request):
    qs = Pedido.objects.select_related("usuario").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def pedido_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = PedidoForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def pedido_update(request, pk):
    obj = get_object_or_404(Pedido, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = PedidoForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def pedido_delete(request, pk):
    obj = get_object_or_404(Pedido, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})


# ====================== RECOPILACIÓN ======================
def recopilacion_list(request):
    qs = Recopilacion.objects.select_related("usuario").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def recopilacion_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = RecopilacionForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def recopilacion_update(request, pk):
    obj = get_object_or_404(Recopilacion, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = RecopilacionForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def recopilacion_delete(request, pk):
    obj = get_object_or_404(Recopilacion, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})

# ====================== CARRITO ======================
def carrito_list(request):
    qs = Carrito.objects.select_related("usuario").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def carrito_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = CarritoForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def carrito_update(request, pk):
    obj = get_object_or_404(Carrito, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    form = CarritoForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def carrito_delete(request, pk):
    obj = get_object_or_404(Carrito, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})


# ====================== CARRITO ITEM ======================
def carritoitem_list(request):
    qs = CarritoItem.objects.select_related("carrito", "cancion", "vinilo").all()
    return JsonResponse({"object_list": json.loads(serialize("json", qs))}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def carritoitem_create(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    # Validar si los IDs existen
    carrito_id = data.get("carrito")
    if carrito_id and not Carrito.objects.filter(pk=carrito_id).exists():
        return JsonResponse({"error": "Carrito no existe"}, status=400)

    cancion_id = data.get("cancion")
    if cancion_id and not Cancion.objects.filter(pk=cancion_id).exists():
        return JsonResponse({"error": "Cancion no existe"}, status=400)

    vinilo_id = data.get("vinilo")
    if vinilo_id and not Vinilo.objects.filter(pk=vinilo_id).exists():
        return JsonResponse({"error": "Vinilo no existe"}, status=400)

    form = CarritoItemForm(data)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def carritoitem_update(request, pk):
    obj = get_object_or_404(CarritoItem, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    form = CarritoItemForm(data, instance=obj)
    if form.is_valid():
        obj = form.save()
        return JsonResponse({"object": json.loads(serialize("json", [obj]))}, safe=False)
    return JsonResponse({"errors": form.errors}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def carritoitem_delete(request, pk):
    obj = get_object_or_404(CarritoItem, pk=pk)
    obj.delete()
    return JsonResponse({"deleted": True})