from django.db import models
from django.conf import settings #Importa usuario personalizado


class Categoria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre
    
    #Clase Juego == Post
class Juego(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='juego', null=True, blank=True)
    titulo = models.CharField(max_length=45, null=False, blank=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='juegos_imagenes/',
                                null=True,
                                blank=True,
                                default='profiles/perfil-default.jpg')
    archivo = models.FileField(upload_to='juego/', null=True, blank=True)

    es_reseña = models.BooleanField(default=False)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    def __str__(self):
        return self.titulo
    
    def total_likes(self):
        return self.likes.count()
