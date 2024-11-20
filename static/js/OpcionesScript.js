document.addEventListener("DOMContentLoaded", function () {
    // Referencias a los elementos
    const estadoMaquinariaSpan = document.getElementById("estado-maquinaria");
    const mantenimientoTextarea = document.getElementById("mantenimiento-textarea");
    const guardarBoton = document.getElementById("guardar-boton");
    const botonesEstado = document.querySelectorAll(".estado-boton");

    // Verifica que los elementos existan antes de proceder
    if (!estadoMaquinariaSpan || !mantenimientoTextarea || !guardarBoton || botonesEstado.length === 0) {
        console.error("Algunos elementos necesarios no fueron encontrados. Revisa los IDs y clases en el HTML.");
        return;
    }

    // Manejar clic en botones de estado (excluyendo el botón Rentar)
    botonesEstado.forEach((boton) => {
        if (boton.textContent.trim() === "Rentar") {
            // Excluir el botón Rentar de esta lógica
            return;
        }
        boton.addEventListener("click", () => {
            const nuevoEstado = boton.getAttribute("data-estado"); // Obtener el estado del atributo data-estado
            if (nuevoEstado) {
                estadoMaquinariaSpan.textContent = nuevoEstado; // Cambiar el texto visible
            }
        });
    });

    // Manejar clic en el botón Guardar
    guardarBoton.addEventListener("click", function () {
        // Obtener valores actuales
        const estadoActual = estadoMaquinariaSpan.textContent; // Estado visible en el DOM
        const mantenimientoInfo = mantenimientoTextarea.value; // Texto ingresado en el textarea

        // Crear un objeto FormData para enviar al servidor
        const formData = new FormData();
        formData.append("estado", estadoActual);
        formData.append("informacion_mantenimiento", mantenimientoInfo);

        // Enviar datos con fetch
        fetch(window.location.href, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Obtener el token CSRF desde las cookies
            },
        })
            .then((response) => {
                if (response.ok) {
                    return response.text();
                }
                throw new Error("Error al guardar los datos en el servidor.");
            })
            .then(() => {
                alert("Cambios guardados correctamente.");
                window.location.href = "/Inventario/"; // Redirigir al inventario
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Ocurrió un error al guardar los datos.");
            });
    });

    // Función para obtener el CSRF token de las cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});