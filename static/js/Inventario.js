function confirmarEliminacion(maquinariaId) {
    const confirmacion = confirm("¿Estás seguro de que deseas eliminar esta maquinaria?");
    if (confirmacion) {
        // Redirigir a la URL de eliminación
        window.location.href = `/EliminarMaquinaria/${maquinariaId}/`;
    }
}