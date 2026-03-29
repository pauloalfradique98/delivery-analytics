document.addEventListener("DOMContentLoaded", function () {

    console.log("JS carregou");

    console.log(horasLabels, horasValores);

    const ctx1 = document.getElementById('graficoHorarios');

    if (ctx1 && horasLabels && horasValores) {
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: horasLabels,
                datasets: [{
                    label: 'Entregas',
                    data: horasValores,
                    backgroundColor: '#2d89ef'
                }]
            }
        });
    }

    const ctx2 = document.getElementById('graficoBairros');

    if (ctx2 && bairrosLabels && bairrosValores) {
        new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: bairrosLabels,
                datasets: [{
                    data: bairrosValores
                }]
            }
        });
    }

    const formAdd = document.getElementById("form-add");

    if (formAdd) {
        formAdd.addEventListener("submit", function(e) {
            const btn = this.querySelector("button[type='submit']");
            btn.disabled = true;
        });
    }

});