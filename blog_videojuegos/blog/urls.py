from django.urls import path
from  . import views

urlpatterns = [
    path('', views.post_juego, name='blog'),
    path('', views.lista_juegos, name='blog')
]