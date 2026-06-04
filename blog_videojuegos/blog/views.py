from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Juego
from .forms import PostJuego
from .models import Categoria

# Create your views here.
    
def lista_juegos(request):
    juegos = Juego.objects.all().order_by('-id') #Mantenemos un orden consistente
    paginator = Paginator(juegos, 8) #Mostramos 8 juegos por paginas
    #Obtenbemos el numero de paginas desde la URL (?page=2)
    page_number = request.GET.get('page')
    #Obetnemos los objetos de esa pagina
    page_obj = paginator.get_page(page_number)
    #Pasamos a la plantilla como lista_juegos
    contexto_blog_juegos = {'lista_juegos': page_obj}
    return render(request, 'blog/blog.html', contexto_blog_juegos)

def detalle_juego(request, pk):
    #Obtenemos el juego concreto o un 404 si no existe
    juego = get_object_or_404(Juego, pk=pk)

    #Creamos el contexto que pasaremos a la plantilla
    contexto = {'juego': juego}

    #Renderizamos la pantillade detalle
    return render(request, 'blog/detalle_juego.html', contexto)

# Vista Crear_post
@login_required
def crear_post(request):
    if request.method == 'POST': 
        form = PostJuego(request.POST, request.FILES) #Recibimos los datos del formulario
        if form.is_valid():
            juego = form.save(commit=False) #Frenamos el guardado para inyectar el autor de la sesion
            juego.autor = request.user # Asignacion segura del usuario logueado
            juego.save() #Guardado en base de datos

            messages.success(request, "¡Tu juego se publicó con éxito en The Glitch Zone!")
            return redirect('blog:blog') # Reddireccion a la lista de videojuegos
    else:
        form = PostJuego()


        return render(request, 'blog/crear_post.html', {'form': form})

