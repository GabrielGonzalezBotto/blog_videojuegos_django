from django.shortcuts import render

# Create your views here.
def post_juego(request):
    juegos = [
        {'nombre_usuario': 'Gabriel Gonzalez Botto', 'fecha': '22/02/26', 'nombre': 'Battletoads', 'plataforma':'SEGA genesis'},
        {'nombre_usuario': 'Martina Gonzalez', 'fecha': '15/02/26', 'nombre': 'Boogerman', 'plataforma': 'SEGA genesis'},
        {'nombre_usuario': 'Josefina Botto', 'fecha': '2/02/26', 'nombre': 'Cadillacs & Dinosaurs', 'plataforma': 'ARCADE'},
        {'nombre_usuario': 'Jorge Gonzalez', 'fecha': '23/02/26', 'nombre': 'Bloody Roar', 'plataforma': 'PlayStation'},
        {'nombre_usuario': 'Jorge Gonzalez', 'fecha': '23/02/26', 'nombre': 'Bloody Roar', 'plataforma': 'PlayStation'},
        {'nombre_usuario': 'Josefina Botto', 'fecha': '2/02/26', 'nombre': 'Cadillacs & Dinosaurs', 'plataforma': 'ARCADE'},
    ]

    contexto_post_juego = {'post_juego': juegos}
    return render(request, 'blog/blog.html', contexto_post_juego)