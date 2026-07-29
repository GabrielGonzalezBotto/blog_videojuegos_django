from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from  .forms import RegistroForm, LoginForm, EditarPerfilForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from blog.models import Juego, Categoria
from django.db.models import Sum

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
    usuario_actual = request.user

    # --- 1. LÓGICA DE EDICIÓN POST (Dejas quieto todo tu código actual aquí) ---
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

    # --- 2. ⚡ NUEVO: MOTOR DE FILTRADO, ORDENAMIENTO Y PAGINACIÓN DEL PERFIL ---
    # Traemos todos tus juegos directos anotando el conteo de comentarios de fondo
    mis_juegos_queryset = usuario_actual.juego.all().annotate(total_comentarios=Count('comentario'))
    total_likes_data = Juego.objects.filter(autor=request.user).aggregate(total=Count('likes'))
    total_likes = total_likes_data['total'] if total_likes_data['total'] else 0

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

    # D. EL PAGINADOR (Corta en 4 tarjetas por página)
    paginator = Paginator(mis_juegos_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 3. CONTEXTO COMPLETO PARA EL RENDERING
    contexto = {
        'form': form,
        'mis_juegos': page_obj,
        'categorias': Categoria.objects.all(),
        'total_likes': total_likes
    }
    return render(request, 'usuarios/perfil.html', contexto)