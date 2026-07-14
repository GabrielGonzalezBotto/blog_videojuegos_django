// BOTON IR ARRIBA
document.addEventListener('DOMContentLoaded', function () {
    const label = document.querySelector('.ir');
    const checkbox = document.querySelector('.toggle-neon');

    if (!label || !checkbox) {
        console.error('Error: No se encontró .ir o .toggle-neon. Verifica el HTML.');
        return;
    }

    // Evento de clic para encender el neón y subir
    label.addEventListener('click', function () {
        checkbox.checked = true; // Enciende el neón
        console.log('Clic en el botón, neón encendido, checked:', checkbox.checked);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Manejador de scroll
    window.addEventListener('scroll', function () {
        try {
            if (window.scrollY > 100) {
                label.style.display = 'block';
                //checkbox.checked = false; // Apaga el neón al reaparecer//estuve toda la tarde viendo cual era el error del encendido del neon y era esta linea que hace que el neon se apague cuando soltas el click!
                console.log('Scroll > 100: Botón mostrado, neón apagado, checked:', checkbox.checked);
            } else if (window.scrollY <= 100) {
                label.style.display = 'none';
                checkbox.checked = false; // Apaga el neón al ocultar
                console.log('Scroll <= 100: Botón oculto, neón apagado, checked:', checkbox.checked);
            }
        } catch (error) {
            console.error('Error en el manejador de scroll:', error);
        }
    });
});

//FILTROS

document.addEventListener('DOMContentLoaded', function () {
    const filtroBotones = document.querySelectorAll('.filtro-btn');
    const tipoBotones = document.querySelectorAll('.filtro-tipo-btn');
    const filtroGrupos = document.querySelectorAll('.filtro-grupo');
    const carruselTrack = document.querySelector('.carrusel-track');

    // ⚡ 1. Código corto para mover el carrusel (Mantenemos tus flechas funcionales)
    document.querySelector('.prev-btn').addEventListener('click', () => carruselTrack.scrollBy({ left: -100, behavior: 'smooth' }));
    document.querySelector('.next-btn').addEventListener('click', () => carruselTrack.scrollBy({ left: 100, behavior: 'smooth' }));

    // ⚡ 2. Intercambio visual de los grupos (Categorías, Post, Comentarios)
    tipoBotones.forEach(boton => {
        boton.addEventListener('click', () => {
            tipoBotones.forEach(btn => btn.classList.remove('active'));
            boton.classList.add('active');

            filtroGrupos.forEach(grupo => grupo.classList.remove('active'));
            const grupoDestino = document.querySelector(`.filtro-grupo.${boton.dataset.tipo}`);
            if (grupoDestino) grupoDestino.classList.add('active');
        });
    });

    // ⚡ 3. LA MAGIA: Al hacer clic, redirige agregando el filtro a la URL de Django
    filtroBotones.forEach(boton => {
        boton.addEventListener('click', () => {
            const tipo = boton.dataset.filtro; // 'categoria', 'fecha' o 'comentarios'
            const urlActual = new URL(window.location.href);

            if (tipo === 'categoria') {
                const cat = boton.dataset.categoria;
                if (cat === 'all') urlActual.searchParams.delete('categoria');
                else urlActual.searchParams.set('categoria', cat);
            } 
            else if (tipo === 'fecha') {
                urlActual.searchParams.set('orden_fecha', boton.dataset.orden);
                urlActual.searchParams.delete('orden_comentarios'); // Limpia el otro orden
            } 
            else if (tipo === 'comentarios') {
                urlActual.searchParams.set('orden_comentarios', boton.dataset.orden);
                urlActual.searchParams.delete('orden_fecha'); // Limpia el otro orden
            }

            // Resetea la página a la 1 cada vez que se aplica un filtro nuevo
            urlActual.searchParams.delete('page');

            // Redirige la pestaña automáticamente
            window.location.href = urlActual.toString();
        });
    });
});

//LIKES
document.addEventListener('DOMContentLoaded', function () {
    const likeForms = document.querySelectorAll('.like-form');

    likeForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault(); 

            const url = this.getAttribute('action');
            const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;

            const checkbox = this.querySelector('.like-checkbox');
            const juegoId = checkbox.dataset.id;
            const corazonIcono = this.querySelector('.fa-heart');
            const contadorSpan = document.getElementById(`like-count-${juegoId}`); // ⚡ Nombre base: contadorSpan

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
            .then(response => {
                if (!response.ok || response.status === 403) {
                    mostrarModalLogin(); 
                    throw new Error("Usuario no autenticado");
                }
                return response.json();
            })
            .then(data => {
                if (data) {
                    // ⚡ CORREGIDO: Cambiamos 'countEl' por 'contadorSpan' para que matchee con la variable de arriba
                    if (contadorSpan) contadorSpan.textContent = data.total_likes;
                    
                    checkbox.checked = data.liked;
                    if (data.liked) {
                        if (corazonIcono) corazonIcono.classList.add("liked");
                    } else {
                        if (corazonIcono) corazonIcono.classList.remove("liked");
                    }
                }
            })
            .catch(error => console.warn(error.message));
        });
    });

    const likeLabels = document.querySelectorAll('.like-label');
    likeLabels.forEach(label => {
        label.addEventListener('click', function(e) {
            e.preventDefault(); 
            const formAsociado = this.closest('.like-form');
            formAsociado.dispatchEvent(new Event('submit')); 
        });
    });
});

//CARTEL REGISTRO/LOGIN LIKE
function mostrarModalLogin() {
    document.getElementById('modal-login-glitch').style.display = 'flex';
}
function cerrarModalLogin() {
    document.getElementById('modal-login-glitch').style.display = 'none';
}
// Cierra también si hacen clic afuera del cuadro negro
window.onclick = function(event) {
    const modal = document.getElementById('modal-login-glitch');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}