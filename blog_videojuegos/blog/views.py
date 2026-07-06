from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Juego, Categoria, Comentario
from .forms import PostJuego
from  django.db.models import Count, Q

# Create your views here.
    
def lista_juegos(request):
    juegos_queryset = Juego.objects.all().annotate(total_comentarios=Count('comentario'))
    palabra_clave = request.GET.get('q', '').strip()
    if palabra_clave:
        juegos_queryset = juegos_queryset.filter(
            Q(titulo__icontains=palabra_clave) |
            Q(descripcion__icontains=palabra_clave)
        ).distinct()
    categoria_filtrada = request.GET.get('categoria')
    if categoria_filtrada:
        juegos_queryset = juegos_queryset.filter(categoria__nombre__iexact=categoria_filtrada)

    #ORDEN POR FECHA
    orden_fecha = request.GET.get('orden_fecha')
    if orden_fecha == 'reciente':
        juegos_queryset = juegos_queryset.order_by('-id')
    elif orden_fecha == 'antiguo':
        juegos_queryset = juegos_queryset.order_by('id')

    #ORDEN POR COMENTARIOS
    orden_comentarios = request.GET.get('orden_comentarios')
    if orden_comentarios == 'mas':
        juegos_queryset = juegos_queryset.order_by('-total_comentarios')
    elif orden_comentarios == 'menos':
        juegos_queryset = juegos_queryset.order_by('total_comentarios')
    
    #ID DESCENDENTE, SI NO HAY ORDEN
    if not orden_fecha and not orden_comentarios:
        juegos_queryset = juegos_queryset.order_by('-id')

    #PAGINATOR
    paginator = Paginator(juegos_queryset, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #ENVIAMOS CATEGORIAS PARA QUE FUNCIONEN LOS BOTONES
    contexto_blog_juegos = {
        'lista_juegos': page_obj,
        'categorias': Categoria.objects.all()
    }
    return render(request, 'blog/blog.html', contexto_blog_juegos)

def detalle_juego(request, pk):
    juego = get_object_or_404(Juego, pk=pk)

    if request.method == 'POST' and request.user.is_authenticated:
        texto_comentario = request.POST.get('comentario', '').strip()

        if texto_comentario: #Si el usuario envia un comentario y no un espacoi vacio
            Comentario.objects.create(
                usuario=request.user,
                blog=juego,
                texto=texto_comentario
            )
            messages.success(request, "¡Tu comentario se publicó con exito!")
            return redirect('blog:detalle_juego', pk=juego.pk)
    
    comentarios = juego.comentario.all()

    contexto = {'juego': juego,
                'comenetarios': comentarios}
    return render(request, 'blog/detalle_juego.html', contexto)

# Vista Crear_post
@login_required
def crear_post(request):
    if request.method == 'POST': 
        form = PostJuego(request.POST, request.FILES) 
        
        if form.is_valid():
            juego = form.save(commit=False) 
            juego.autor = request.user      
            
            # 💡 Sincronizado con la BD: Buscamos usando 'nueva_categoria' y la tabla 'Categoria'
            nombre_manual = request.POST.get('nueva_categoria', '').strip()
            id_desplegable = request.POST.get('categoria') 

            if nombre_manual:
                # Usa 'nombre', que es como se llama en tu base de datos física
                categoria_objeto, creada = Categoria.objects.get_or_create(nombre=nombre_manual)
                juego.categoria = categoria_objeto
            elif id_desplegable:
                try:
                    juego.categoria = Categoria.objects.get(id=id_desplegable)
                except Categoria.DoesNotExist:
                    pass

            juego.save() # ¡Guardado definitivo!
            
            messages.success(request, "¡Tu juego se publicó con éxito en The Glitch Zone!")
            return redirect('blog:blog') 
    else:
        form = PostJuego()

    return render(request, 'blog/crear_post.html', {
        'form': form,
        'categorias': Categoria.objects.all() # Pasamos las categorías existentes
    })

@login_required
def editar_post(request,pk):
    juego = get_object_or_404(Juego, pk=pk) #Buscamos el juego o tiramos 404 si no existe

    if juego.autor != request.user:
        messages.error(request, "No tenés permisos para editar este videojuego.")
        return redirect ('blog:blog')
    
    if request.method == 'POST':
        form = PostJuego(request.POST, request.FILES, instance=juego) #Pasamos instance=juego para que django actualice y no cree uno nuevo
        if form.is_valid():
            juego_editado = form.save(commit=False) #Frenamos el guardado un segundo para ingresar la categoria(plataforma), manualmente
            nombre_manual = request.POST.get('nueva_categoria', '').strip() #Logica de categoria manual(igual a crear_post)
            id_desplegable = request.POST.get('categoria')
            
            if nombre_manual:
                categoria_objeto, creada = Categoria.objects.get_or_create(nombre=nombre_manual)
                juego_editado.categoria = categoria_objeto
            elif id_desplegable:
                try:
                    juego_editado.categoria = Categoria.objeto.get(id=id_desplegable)
                except Categoria.DoesNotExist:
                    pass
            else:
                juego_editado.categoria = None #Si usuario borra todo y no selecciona nada, podems dejar en None

            juego_editado.save()

            messages.success(request, "¡Tu posteo se actualizó correctamente!")
            return redirect('blog:blog')
    else:
        form = PostJuego(instance=juego)

    return render(request, 'blog/editar_post.html', {
        'form': form,
        'juego': juego,
        'categoria': Categoria.objects.all()
    })

@login_required
def eliminar_post(request, pk):
    juego = get_object_or_404(Juego, pk=pk)

    if juego.autor != request.user: 
        messages.error(request, "No tenés permisos para eliminar este videojuego.")
        return redirect('blog:blog') #Volvemos a blog
    
    if request.method == 'POST':
        juego.delete() #borrado fisico de la base de datos
        messages.success(request, "El post fue eliminado correctamente.")
        return redirect('blog:blog') #Volvemos a blog
    
    return render(request, 'blog/eliminar_post.html', {'juego': juego})

@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    id_juego = comentario.blog.pk

    if comentario.usuario != request.user:
        messages.error(request, "No tienes permisos para borrar este comentario.")
        return redirect('blog:detalle_juego', pk=id_juego)
    
    if request.method == 'POST':
        comentario.delete()
        messages.success(request, "¡Tu comentario fue eliminado con éxito!")
        return redirect('blog:detalle_juego', pk=id_juego)
    
    return render(request, 'blog/eliminar_comentario.html',{
        'comentario':comentario,
        'id_juego': id_juego
    })

@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    id_juego = comentario.blog.pk

    if comentario.usuario != request.user:
        messages.error(request, "No tenés permisos para editar este comentario.")
        return redirect('blog:detalle_juego', pk=id_juego)
    
    if request.method == 'POST':
        nuevo_texto = request.POST.get('texto_comentario', '').strip()

        if nuevo_texto:
            comentario.texto = nuevo_texto
            comentario.save()
            messages.success(request, "¡Tu comentario se actualizó correctamente!")
        else:
            messages.error(request, "El comentario no puede estar vacío.")
        
        return redirect('blog:detalle_juego', pk=id_juego)
    
    return render(request, 'blog/editar_comentario.html', {
        'comentario': comentario,
        'id_juego': id_juego
    })



#def crear_post(request):
    #if request.method == 'POST': 
        #form = PostJuego(request.POST, request.FILES) #Recibimos los datos del formulario
        #if form.is_valid():
            #juego = form.save(commit=False) #Frenamos el guardado para inyectar el autor de la sesion
            #juego.autor = request.user # Asignacion segura del usuario logueado
            #juego.save() #Guardado en base de datos

            #messages.success(request, "¡Tu juego se publicó con éxito en The Glitch Zone!")
            #return redirect('blog:blog') # Reddireccion a la lista de videojuegos
    #else:
        #form = PostJuego()


    #return render(request, 'blog/crear_post.html', {'form': form})

