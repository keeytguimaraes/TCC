// ==========================
// ESCONDER TODAS AS OPÇÕES
// ==========================
function esconderTudo() {

    document.getElementById(
        "div_receber"
    ).style.display = "none";

    document.getElementById(
        "div_fiado"
    ).style.display = "none";

    document.getElementById(
        "div_pendente"
    ).style.display = "none";
}

// ==========================
// REMOVE CARD ATIVO
// ==========================
function removerSelecao() {

    document
        .getElementById("card_receber")
        .classList
        .remove("ativo");

    document
        .getElementById("card_fiado")
        .classList
        .remove("ativo");

    document
        .getElementById("card_pendente")
        .classList
        .remove("ativo");
}

// ==========================
// RECEBER AGORA
// ==========================
function mostrarReceber() {

    esconderTudo();

    removerSelecao();

    document
        .getElementById("card_receber")
        .classList
        .add("ativo");

    document.getElementById(
        "div_receber"
    ).style.display = "block";
}

// ==========================
// VENDA FIADO
// ==========================
function mostrarFiado() {

    esconderTudo();

    removerSelecao();

    document
        .getElementById("card_fiado")
        .classList
        .add("ativo");

    document.getElementById(
        "div_fiado"
    ).style.display = "block";

    if (!$('.select-cliente').hasClass("select2-hidden-accessible")) {

        $('.select-cliente').select2({

            placeholder: "Pesquisar cliente...",

            width: '100%'
        });

    }

}

// ==========================
// CONTA PENDENTE
// ==========================
function mostrarPendente() {

    esconderTudo();

    removerSelecao();

    document
        .getElementById("card_pendente")
        .classList
        .add("ativo");

    document.getElementById(
        "div_pendente"
    ).style.display = "block";
}


// ==========================
// SELECT2 CLIENTES
// ==========================

function iniciarSelectCliente(){

    $('.select-cliente').select2({

        placeholder: "Pesquisar cliente...",

        width: '100%'
    });

}