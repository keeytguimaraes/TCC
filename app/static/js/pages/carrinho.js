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
// DESCONTO GERAL DA VENDA
// ==========================

// Campo onde o usuário digita o desconto
const campoDesconto =
document.querySelector(
    'input[name="desconto_venda"]'
);

// Se o campo existir na página
if (campoDesconto) {

    // Atualiza sempre que o valor mudar
    campoDesconto.addEventListener(
        "input",
        atualizarResumoVenda
    );

    // Executa uma vez ao abrir a página
    atualizarResumoVenda();
}


// ==========================
// ATUALIZA RESUMO DA VENDA
// ==========================
function atualizarResumoVenda(){

    // Busca o valor total bruto
    const textoTotal =
        document.getElementById(
            "total-bruto"
        ).innerText;

    const totalBruto =
        parseFloat(
            textoTotal
            .replace("R$","")
            .replace(",",".")
        );

    // Valor digitado no desconto
    let desconto =
        parseFloat(
            campoDesconto.value
        );

    // Se estiver vazio
    if(isNaN(desconto)){

        desconto = 0;
    }

    // Calcula total final
    let totalFinal =
        totalBruto - desconto;

    // Não deixa ficar negativo
    if(totalFinal < 0){

        totalFinal = 0;
    }

    // ----------------------
    // Atualiza desconto
    // ----------------------
    const valorDesconto =
        document.getElementById(
            "valor-desconto"
        );

    valorDesconto.innerText =
        "R$ " +
        desconto.toFixed(2);

    valorDesconto.style.color =
        "#dc3545";

    valorDesconto.style.fontWeight =
        "bold";

    // ----------------------
    // Atualiza total final
    // ----------------------
    const valorFinal =
        document.getElementById(
            "valor-final"
        );

    valorFinal.innerText =
        "R$ " +
        totalFinal.toFixed(2);

    valorFinal.style.color =
        "#198754";

    valorFinal.style.fontWeight =
        "bold";
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

