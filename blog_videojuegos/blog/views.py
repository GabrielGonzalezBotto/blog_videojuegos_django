from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Juego

# Create your views here.
def post_juego(request):
    juegos = Juego.objects.all()
    contexto_post_juego = {'post_juego': juegos}
    return render(request, 'blog/blog.html', contexto_post_juego)

def lista_post(request):
    juegos = Juego.objects.all().order_by('id') #Mantenemos un orden consistente
    paginator = Paginator(Juego, 8) #Mostramos juegos por pagina
    page_number = request.GET.get('page') #Obtenemos el numero de pagina desde la URL (?page=2)
    page_obj = paginator.get_page(page_number) #Obtenemos los objetos de esa pagina
    #Pasamos a plantilla como 'lista_post'
    contexto_post_juego = {'lista_post': page_obj}
    return render(request, 'blog/blog.html', contexto_post_juego)
