from django.db import models

# Create your models here.
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    decha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.email}"
