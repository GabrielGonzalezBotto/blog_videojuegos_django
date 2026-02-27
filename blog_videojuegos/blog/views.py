from django.shortcuts import render

# Create your views here.
def post_juego(request):
    juegos = [
        {'nombre': 'Battletoads', 'plataforma':'SEGA genesis'},
        {'nombre': 'Boogerman', 'plataforma': 'SEGA genesis'},
        {'nombre': 'Cadillacs & Dinosaurs', 'plataforma': 'ARCADE'},
        {'nombre': 'Bloody Roar', 'plataforma': 'PlayStation'}
    ]

    contexto_post_juego = {'post_juego': juegos}
    return render(request, 'blog/post_juego.html', contexto_post_juego)