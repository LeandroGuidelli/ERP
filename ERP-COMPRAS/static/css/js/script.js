document.addEventListener("DOMContentLoaded", function () {
    atualizarTabela();
    atualizarGraficos();
});

const ctxBar = document.getElementById("estoqueChart").getContext("2d");
const ctxPie = document.getElementById("estoquePieChart").getContext("2d");

let chartBar = new Chart(ctxBar, {
    type: "bar",
    data: { labels: [], datasets: [{ label: "Quantidade", data: [], backgroundColor: ["#007bff"], borderWidth: 1 }] },
    options: { responsive: true, scales: { y: { beginAtZero: true } } }
});

let chartPie = new Chart(ctxPie, {
    type: "doughnut",
    data: { labels: [], datasets: [{ data: [], backgroundColor: ["#007bff", "#28a745", "#dc3545", "#ffc107"] }] },
    options: { responsive: true }
});

function atualizarTabela() {
    fetch("/estoque")
        .then(res => res.json())
        .then(data => {
            let tabela = document.getElementById("estoqueTabela");
            tabela.innerHTML = "";
            for (let material in data) {
                tabela.innerHTML += `<tr><td>${material}</td><td>${data[material]}</td></tr>`;
            }
            atualizarGraficos(data);
        });
}

function atualizarGraficos(data = {}) {
    let materiais = Object.keys(data);
    let quantidades = Object.values(data);

    chartBar.data.labels = materiais;
    chartBar.data.datasets[0].data = quantidades;
    chartBar.update();

    chartPie.data.labels = materiais;
    chartPie.data.datasets[0].data = quantidades;
    chartPie.update();
}

function enviarDados(url, dados) {
    return fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    }).then(res => res.json());
}

function adicionarCompra() {
    let material = document.getElementById("material").value.trim();
    let quantidade = parseInt(document.getElementById("quantidade").value);

    if (material && quantidade > 0) {
        enviarDados("/adicionar_compra", { material, quantidade }).then(() => atualizarTabela());
    } else {
        alert("Preencha os campos corretamente.");
    }
}
