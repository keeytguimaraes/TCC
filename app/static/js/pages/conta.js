function abrirModalTransferir(contaId) {

    document
        .getElementById("modal-transferir")
        .style.display = "flex";

    document
        .getElementById("form-transferir")
        .action =
        "/conta/transferir/confirmar/" + contaId;
}

function fecharModalTransferir() {

    document
        .getElementById("modal-transferir")
        .style.display = "none";
}