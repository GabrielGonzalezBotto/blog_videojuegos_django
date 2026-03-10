from django.urls import path
from  . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('contacto/', views.contacto, name='contacto'),
    path('nosotros/', views.nosotros, name='nosotros'),
]