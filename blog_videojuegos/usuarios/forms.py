from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', ]


class LoginForm(AuthenticationForm):
    # No hace falta Meta
    pass

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['imagen_perfil', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'row': 3, 'placeholder': 'Contanos sobre vos...'}),
        }