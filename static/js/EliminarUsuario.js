document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("usuario-form");
    const btnRegistrar = document.getElementById("btn-registrar");
    const btnActualizar = document.getElementById("btn-actualizar");

    const actualizarBtns = document.querySelectorAll(".btn-actualizar");
    const eliminarBtns = document.querySelectorAll(".btn-eliminar");

    actualizarBtns.forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const id = btn.dataset.id;

            // Cargar datos en el formulario
            form.action = `/ActualizarUsuarios/${id}/`;
            document.getElementById("usuario-id").value = id;
            document.querySelector("[name='nombre']").value = btn.dataset.nombre;
            document.querySelector("[name='segundo_nombre']").value = btn.dataset.segundoNombre || "";
            document.querySelector("[name='apellido']").value = btn.dataset.apellido;
            document.querySelector("[name='segundo_apellido']").value = btn.dataset.segundoApellido || "";
            document.querySelector("[name='correo_electronico']").value = btn.dataset.correo;

            // Cambiar botones
            btnRegistrar.style.display = "none";
            btnActualizar.style.display = "block";
        });
    });

    eliminarBtns.forEach((btn) => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            const id = btn.dataset.id;

            if (confirm("¿Estás seguro de que deseas eliminar este usuario?")) {
                window.location.href = `/EliminarUsuario/${id}/`;
            }
        });
    });
});