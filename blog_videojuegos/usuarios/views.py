from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from  .forms import RegistroForm, LoginForm, EditarPerfilForm
from django.contrib import messages

# Create your views here.
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
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
#def perfil_view(request):
    #return render(request, 'usuarios/editar_perfil.html')
def perfil(request):
    if request.method == 'POST':
        # instance=request.user le indica a Django que actualice al usuario actual en vez de crear uno nuevo
        # request.FILES es obligatorio para recibir archivos multimedia como imágenes
        form = EditarPerfilForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil e imagen se actualizaron correctamente!")
            return redirect('perfil')
    else:
        # Carga el formulario con los datos actuales del usuario logueado
        form = EditarPerfilForm(instance=request.user)
        
    return render(request, 'usuarios/editar_perfil.html', {'form': form})