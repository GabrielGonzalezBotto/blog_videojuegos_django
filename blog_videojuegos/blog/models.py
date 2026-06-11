import os
import uuid
from django.db import models
from django.conf import settings 
from django.contrib.auth.models import User
from django.templatetags.static import static

class Perfil(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='profiles/perfil-default.jpg')

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    

def generar_ruta_unica(instance, filename):
    extension = filename.split('.')[-1]
    nombre_unico = f"{uuid.uuid4()}.{extension}"
    return os.path.join('juegos_imagenes', models.functions.Now().date().strftime('%Y/%m'), nombre_unico)

class Categoria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre
    
class Juego(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='juego', null=True, blank=True)
    titulo = models.CharField(max_length=45, null=False, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True) 
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to=generar_ruta_unica, null=True, blank=True, default='profiles/perfil-default.jpg')
    archivo = models.FileField(upload_to='juego/', null=True, blank=True)
    es_reseña = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    # ⚡ MODIFICADO: Estos métodos volvieron adentro de la clase Juego que es su dueña real
    @property
    def obtener_avatar_url(self):
        try:
            if self.autor and self.autor.imagen_perfil:
                return self.autor.imagen_perfil.url
        except Exception:
            pass
        return static('img/profiles/perfil-DEFAULT.jpg')

    def __str__(self):
        return self.titulo
    
    def total_likes(self):
        return self.likes.count()

# modelo Comentario
class Comentario(models.Model):
    # Usamos settings.AUTH_USER_MODEL para que se conecte directo con tu app de usuarios
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='comentario')
    texto = models.TextField(verbose_name='Comentario')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username}: {self.texto[:20]}"
    
    class Meta:
        ordering = ['-fecha',]