from django.urls import path
from  . import views

app_name = 'blog'

urlpatterns = [
    path('', views.lista_juegos, name='blog'),
    path('juego/<int:pk>/', views.detalle_juego, name='detalle_juego'),
    path('crear/', views.crear_post, name='crear_post'),
]