import os
import uuid
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='profiles/perfil-default.jpg')

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    

def generar_ruta_unica(instance, filename):
    extension = filename.split('.')[-1]
    # Genera un código único como 'a1b2c3d4-e5f6...'
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    # Lo guarda en subcarpetas por año y mes (ej: juegos_imagenes/2026/06/nombre_unico.jpg)
    return os.path.join('juegos_imagenes', models.functions.Now().date().strftime('%Y/%m'), nombre_unico)

class Categoria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre
    
class Juego(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='juego', null=True, blank=True)
    titulo = models.CharField(max_length=45, null=False, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True) # 💡 Cambiado a categoria
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='juegos_imagenes/', null=True, blank=True, default='profiles/perfil-default.jpg')
    archivo = models.FileField(upload_to='juego/', null=True, blank=True)
    es_reseña = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    @property
    def obtener_avatar_url(self):
        try:
            # Si el autor tiene perfil y subió un avatar, devolvemos su URL multimedia
            if self.autor and self.autor.perfil and self.autor.perfil.avatar:
                return self.autor.perfil.avatar.url
        except Exception:
            pass
        
        # ⚡ SOLUCIÓN: Si no hay perfil o avatar, devolvemos la ruta exacta a tus archivos estáticos
        return f"{settings.STATIC_URL}img/profiles/perfil-default.jpg"

    def __str__(self):
        return self.titulo
    
    def total_likes(self):
        return self.likes.count()
    
