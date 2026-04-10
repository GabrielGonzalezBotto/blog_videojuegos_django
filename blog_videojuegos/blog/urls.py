from django.urls import path
from  . import views

urlpatterns = [
    path('', views.lista_juegos, name='blog'),
    path('juego/<int:pk>/', views.detalle_juego, name='detalle_juego'),
]