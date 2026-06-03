from django import forms
from .models import Juego, Categoria

class PostJuego(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['titulo', 'imagen', 'categoria', 'descripcion']

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'inputfield',
                'id': 'titulo',
                'placeholder': 'Título',
                'required': 'required',
                }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'file-input',
                'id': 'post-pic-input',
                'accept': 'image/*',
                'style': 'display:none;',
                }),
            'categoria': forms.Select(attrs={
                'class': 'select-field',
                'id': 'categoria',
                }),
            'descripcion': forms.Textarea(attrs={
                'class': 'descripcion',
                'id': 'descripcion',
                'rows': 3,
                'placeholder': 'Cuentanos sobre el juego...',
                'required': 'required',
                'maxlength': '300',
            })
        }