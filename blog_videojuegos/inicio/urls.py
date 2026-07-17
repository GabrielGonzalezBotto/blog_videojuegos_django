from django.urls import path
from . import views

# ⚡ AGREGADO: Definimos el app_name oficial para esta aplicación
app_name = 'inicio'

urlpatterns = [
    # Mantenemos tus rutas idénticas
    path('', views.index, name='index'), # Cambiado name a 'index' para que sea más limpio
    path('contacto/', views.contacto, name='contacto'),
    path('nosotros/', views.nosotros, name='nosotros'),
]