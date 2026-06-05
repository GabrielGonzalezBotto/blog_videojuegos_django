from django import forms
from .models import Juego

class PostJuego(forms.ModelForm):
    class Meta:
        model = Juego
        # 💡 Sincronizado con la base de datos: sacamos el campo del validador para hacerlo manual
        fields = ['titulo', 'imagen', 'descripcion']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'inputfield', 'id': 'titulo', 'placeholder': 'Título', 'required': 'required'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'file-input', 'id': 'post-pic-input', 'accept': 'image/*', 'style': 'display:none;'}),
            'descripcion': forms.Textarea(attrs={'class': 'descripcion', 'id': 'descripcion', 'rows': 3, 'placeholder': 'Cuentanos sobre el juego...', 'required': 'required', 'maxlength': '300'})
        }