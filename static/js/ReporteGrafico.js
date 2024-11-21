document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('reporteChart').getContext('2d');

    const chartData = {
        labels: ['Disponible', 'Rentada', 'En mantenimiento', 'Fuera de servicio'],
        datasets: [{
            data: [reportData.disponible, reportData.rentada, reportData.en_mantenimiento, reportData.fuera_de_servicio],
            backgroundColor: ['#4CAF50', '#FFC107', '#2196F3', '#F44336'],
            borderColor: ['#4CAF50', '#FFC107', '#2196F3', '#F44336'],
            borderWidth: 1
        }]
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                }
            }
        }
    });
});