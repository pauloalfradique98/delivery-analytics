document.addEventListener("DOMContentLoaded", function () {

    console.log("metricas.js carregado");

    const ctx = document.getElementById("graficoDia");

    if (ctx && labelsDia.length > 0) {
        new Chart(ctx, {
            type: "line",
            data: {
                labels: labelsDia,
                datasets: [{
                    label: "Entregas",
                    data: valoresDia,
                    borderColor: "#2d89ef",
                    tension: 0.3,
                    fill: false
                }]
            },
            options: {
                responsive: true
            }
        });
    } else {
        console.log("Sem dados para gráfico");
    }

});