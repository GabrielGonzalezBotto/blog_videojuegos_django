from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from  .forms import RegistroForm, LoginForm, EditarPerfilForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from blog.models import Juego, Categoria


# Create your views here.
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio:index')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio:index')
        else:
            #Mostrar errores generales en consola para debug
            print(form.errors)
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form =  LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def perfil(request):
    # ⚡ CONEXIÓN MAESTRA: Django va a buscar tu modelo personalizado 'Usuario' automáticamente
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # 1. DETECTOR DE CLIC EN EL CREADOR: Atajamos si viene un ID por la URL (?user_id=)
    usuario_id_url = request.GET.get('user_id')

    if usuario_id_url:
        # Si la URL trae un ID, cargamos el perfil de ese creador específico
        usuario_actual = User.objects.get(id=usuario_id_url)
    else:
        # Si no viene ningún ID (entró desde el menú principal), ve su propio perfil
        usuario_actual = request.user

    # --- LÓGICA DE EDICIÓN POST (Tu código original blindado) ---
    if request.method == 'POST':
        if 'eliminar_imagen' in request.POST:
            usuario_actual.imagen_perfil = 'profiles/perfil-default.jpg'
            usuario_actual.save()
            messages.success(request, "¡Tu foto de perfil fue eliminada!")
            return redirect('perfil')
        
        form = EditarPerfilForm(request.POST, request.FILES, instance=usuario_actual)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil se actualizó correctamente!")
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=usuario_actual)

    # --- 2. MOTOR DE FILTRADO, ORDENAMIENTO Y PAGINACIÓN DEL PERFIL ---
    # Traemos todos los juegos directos del 'usuario_actual' (puede ser el tuyo o el del creador clickeado)
    mis_juegos_queryset = usuario_actual.juego.all().annotate(total_comentarios=Count('comentario'))
    
    # Tu consulta ganadora de likes limpia
    total_likes_data = Juego.objects.filter(autor=usuario_actual).aggregate(total=Count('likes'))
    total_likes = total_likes_data['total'] if total_likes_data['total'] else 0

    juegos_favoritos = Juego.objects.filter(likes=usuario_actual).order_by('-id')

    pestaña_activa = request.GET.get('pestaña', 'mis-posts')

    # A. ATAJAR EL FILTRO DE CATEGORÍA DEL CARRUSEL
    categoria_filtrada = request.GET.get('categoria')
    if categoria_filtrada:
        mis_juegos_queryset = mis_juegos_queryset.filter(categoria__nombre__iexact=categoria_filtrada)

    # B. ATAJAR EL ORDEN POR FECHA
    orden_fecha = request.GET.get('orden_fecha')
    if orden_fecha == 'reciente':
        mis_juegos_queryset = mis_juegos_queryset.order_by('-id')
    elif orden_fecha == 'antiguo':
        mis_juegos_queryset = mis_juegos_queryset.order_by('id')

    # C. ATAJAR EL ORDEN POR COMENTARIOS
    orden_comentarios = request.GET.get('orden_comentarios')
    if orden_comentarios == 'mas':
        mis_juegos_queryset = mis_juegos_queryset.order_by('-total_comentarios')
    elif orden_comentarios == 'menos':
        mis_juegos_queryset = mis_juegos_queryset.order_by('total_comentarios')
    
    # ID DESCENDENTE SI NO HAY NINGÚN ORDEN ACTIVO
    if not orden_fecha and not orden_comentarios:
        mis_juegos_queryset = mis_juegos_queryset.order_by('-id')

    # D. ⚡ INTERRUPTOR DEL PAGINADOR DEFINITIVO (Usa de a 6 como te gustaba en el blog)
    if pestaña_activa == 'favoritos':
        paginator = Paginator(juegos_favoritos, 6)
    else:
        paginator = Paginator(mis_juegos_queryset, 6)

    # Capturamos la página actual de la URL y armamos el bloque final de tarjetas
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 3. CONTEXTO COMPLETO PARA EL RENDERING
    # Reemplazamos 'request.user' por 'usuario_actual' en las llaves para que dibuje los datos correctos
    contexto = {
        'form': form,
        'usuario_actual': usuario_actual, # ⚡ CABLE IMPORTANTE PARA EL HTML
        'mis_juegos': page_obj,
        'categorias': Categoria.objects.all(),
        'total_likes': total_likes,
        'pestaña_activa': pestaña_activa,
    }
    return render(request, 'usuarios/perfil.html', contexto)