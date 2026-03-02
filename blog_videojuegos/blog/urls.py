from django.urls import path
from  . import views

urlpatterns = [
    path('', views.post_juego, name='post_juego')
]