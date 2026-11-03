// ============================================================
// FORNECEDORES — confirmação antes de desativar
// ============================================================
// A desativação continua sendo a rota GET já existente
// (/fornecedor/desativar/<id>). Este script apenas pede
// confirmação: preenche o nome no modal e aponta o botão
// "Desativar" para o mesmo link do cartão clicado.
// O modal é aberto pelo componente global (data-modal).
// Sem JavaScript, o link do cartão funciona como antes.
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const gatilho = document.getElementById("abrir-modal-desativar");
    const nome = document.getElementById("desativar-nome");
    const confirmar = document.getElementById("confirmar-desativar");

    if (!gatilho || !nome || !confirmar) return;

    document.querySelectorAll("[data-desativar]").forEach(link => {

        link.addEventListener("click", evento => {

            evento.preventDefault();

            nome.textContent =
                link.dataset.nome || "este fornecedor";

            confirmar.setAttribute(
                "href",
                link.getAttribute("href")
            );

            gatilho.click();

        });

    });

});