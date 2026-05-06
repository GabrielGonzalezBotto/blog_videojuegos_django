from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Nombre de usuario'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Correo electrónico'})
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'placeholder': 'Repetir contraseña'})


class LoginForm(AuthenticationForm):
    # No hace falta Meta
    pass