from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'inicio/index.html')

def contacto(request):
    return render(request, 'inicio/contacto.html')

def nosotros(request):
    return render(request, 'inicio/nosotros.html')