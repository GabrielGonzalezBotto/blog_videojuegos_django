from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from  .forms import RegistroForm, LoginForm, EditarPerfilForm
from django.contrib import messages
from django.core.paginator import Paginator
from blog.models import Juego 

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

    # 1. CONTROLES DE FORMULARIOS POST (Tu código exacto intacto)
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

    # 2. ⚡ REPARACIÓN MAESTRA DEL PAGINADOR EN PYTHON
    # Le pedimos a Python que agarre tus juegos directos vinculados a tu sesión
    lista_juegos_directa = usuario_actual.juego.all().order_by('-id')

    # Activamos el recorte de a 4 tarjetas por página
    paginator = Paginator(lista_juegos_directa, 6) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 3. CONTEXTO ÚNICO PARA RENDERIZAR LA PANTALLA
    contexto = {
        'form': form,
        'mis_juegos': page_obj  # Reutilizamos tu variable para el bucle
    }
    return render(request, 'usuarios/perfil.html', contexto)