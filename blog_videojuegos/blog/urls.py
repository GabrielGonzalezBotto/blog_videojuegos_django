from django.urls import path
from  . import views

app_name = 'blog'

urlpatterns = [
    path('', views.lista_juegos, name='blog'),
    path('juego/<int:pk>/', views.detalle_juego, name='detalle_juego'),
    path('crear/', views.crear_post, name='crear_post'),
    path('post/editar/<int:pk>/', views.editar_post, name='editar_post'),
    path('juego/<int:pk>/eliminar/', views.eliminar_post, name='eliminar_post'),
    path('comentario/eliminar/<int:pk>/', views.eliminar_comentario, name='eliminar_comentario'),
]