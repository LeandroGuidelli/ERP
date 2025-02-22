document.getElementById("nfForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Impede o recarregamento da página

    let formData = new FormData();
    formData.append("data", document.getElementById("data").value);
    formData.append("deposito", document.getElementById("deposito").value);
    formData.append("numero_nf", document.getElementById("numero_nf").value);

    fetch("/adicionar_nf", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensagem) {
            document.getElementById("saida_nf").innerText = data.mensagem;
            document.getElementById("saida_nf").style.color = "green";
        } else if (data.erro) {
            document.getElementById("saida_nf").innerText = data.erro;
            document.getElementById("saida_nf").style.color = "red";
        }
    })
    .catch(error => console.error("Erro:", error));
});