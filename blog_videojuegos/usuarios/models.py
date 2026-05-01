from django.contrib.auth.models import AbstractBaseUser, Group, Permission
from django.db import models

# Create your models here.
class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)

    # Evitar conflictos de reverse accessors
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set', # aqui cambia el related_name
        blank=True,
        help_text='Grupos a los que pertenece este usuario.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_user_set', # aqui cambia el related_name
        blank=True,
        help_text='Permisos especificos para este usuario.',
        verbose_name='user_permissions',
    )

    def __str__(self):
        return self.username