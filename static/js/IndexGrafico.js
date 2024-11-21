document.addEventListener("DOMContentLoaded", function () {
    // Obtener datos dinámicos desde el elemento HTML (usando data-* atributos)
    const chartDataElement = document.getElementById("chart-data");
    const maquinariaData = {
        disponible: parseInt(chartDataElement.dataset.disponible),
        rentada: parseInt(chartDataElement.dataset.rentada),
        en_mantenimiento: parseInt(chartDataElement.dataset.enMantenimiento),
        fuera_de_servicio: parseInt(chartDataElement.dataset.fueraDeServicio),
    };

    // Crear el gráfico circular
    const ctx = document.getElementById("maquinariaChart").getContext("2d");
    const maquinariaChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Disponible", "Rentada", "En mantenimiento", "Fuera de servicio"],
            datasets: [
                {
                    label: "Estado de Maquinarias",
                    data: Object.values(maquinariaData),
                    backgroundColor: ["#4CAF50", "#FFC107", "#2196F3", "#F44336"],
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            let label = context.label || "";
                            if (label) {
                                label += ": ";
                            }
                            label += context.raw || "";
                            return label;
                        },
                    },
                },
            },
        },
    });

    // Convertir el gráfico a imagen para el PDF
    const chartImagePlaceholder = document.getElementById("chart-image-placeholder");
    if (chartImagePlaceholder) {
        const chartImage = ctx.canvas.toDataURL("image/png"); // Convertir el canvas en imagen
        chartImagePlaceholder.src = chartImage; // Asignar la imagen al placeholder
    }
});