from django.shortcuts import render
from django.db.models import Count
from blog.models import Juego

# Create your views here.
def index(request):
    juegos_populares = Juego.objects.annotate(q_likes=Count('likes')).order_by('-q_likes')[:3]
    juegos_recientes = Juego.objects.all().order_by('-id')[:3]
    contexto = {
        'juegos_populares': juegos_populares,
        'juegos_receintes': juegos_recientes
    }
    return render(request, 'inicio/index.html')

def contacto(request):
    return render(request, 'inicio/contacto.html')

def nosotros(request):
    return render(request, 'inicio/nosotros.html')