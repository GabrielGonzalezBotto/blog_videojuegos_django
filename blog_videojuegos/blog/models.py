from django.db import models


# Create your models here.
class Juego(models.Model):
    user = models.CharField(max_length=100)
    fecha = models.DateField(max_length=8)
    nombre = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
