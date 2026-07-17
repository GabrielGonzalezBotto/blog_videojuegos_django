from django.shortcuts import render
from django.db.models import Count
from blog.models import Juego

# Create your views here.
def index(request):
    # 1. Traemos la lista limpia de los juegos ordenados por ID descendente (Los últimos 3 subidos)
    juegos_recientes = Juego.objects.all().order_by('-id')[:3]

    # 2. Traemos los 3 más votados calculando la cantidad de registros en la tabla intermedia de likes
    juegos_populares = Juego.objects.annotate(num_likes=Count('likes')).order_by('-num_likes', '-id')[:3]

    # ⚡ DEBUGEAR EN CONSOLA: Ponemos estos print para ver si Python encuentra los juegos en la terminal
    print(f"--> CANTIDAD DE POPULARES ENCONTRADOS: {juegos_populares.count()}")
    print(f"--> CANTIDAD DE RECIENTES ENCONTRADOS: {juegos_recientes.count()}")

    contexto = {
        'juegos_populares': juegos_populares,
        'juegos_recientes': juegos_recientes
    }
    return render(request, 'inicio/index.html', contexto)

def contacto(request):
    return render(request, 'inicio/contacto.html')

def nosotros(request):
    return render(request, 'inicio/nosotros.html')