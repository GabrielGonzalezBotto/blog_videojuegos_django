from django.shortcuts import render
from blog.models import Juego

# Create your views here.
def post_juego(request):
    juegos = Juego.objects.all()
    contexto_post_juego = {'post_juego': juegos}
    return render(request, 'blog/blog.html', contexto_post_juego)