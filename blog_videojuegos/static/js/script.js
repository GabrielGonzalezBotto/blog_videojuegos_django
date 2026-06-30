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