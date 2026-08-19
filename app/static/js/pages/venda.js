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
// RECEBER AGORA
// ==========================
function mostrarReceber() {

    esconderTudo();

    document.getElementById(
        "div_receber"
    ).style.display = "block";
}


// ==========================
// VENDA FIADO
// ==========================
function mostrarFiado() {

    esconderTudo();

    document.getElementById(
        "div_fiado"
    ).style.display = "block";
}


// ==========================
// CONTA PENDENTE
// ==========================
function mostrarPendente() {

    esconderTudo();

    document.getElementById(
        "div_pendente"
    ).style.display = "block";
}


// ==========================
// EXPANDIR PRODUTO
// ==========================
document
.querySelectorAll(".abrir-card")
.forEach(botao => {

    botao.addEventListener(
        "click",
        () => {

            // Card clicado
            const card =
                botao.closest(
                    ".produto-card"
                );

            // Área expandida do card
            const expandido =
                card.querySelector(
                    ".produto-expandido"
                );

            // Fecha todos os outros cards
            document
            .querySelectorAll(
                ".produto-expandido"
            )
            .forEach(item => {

                if (
                    item !== expandido
                ) {

                    item.classList.remove(
                        "ativo"
                    );

                }

            });

            // Abre ou fecha o card clicado
            expandido.classList.toggle(
                "ativo"
            );

        }
    );

});

// ==========================
// TIPO DE VENDA
// ==========================

document
.querySelectorAll(".tipo-venda-botoes")
.forEach(grupo => {

    const input =
        grupo.parentElement.querySelector(
            ".tipo-venda-input"
        );

    grupo
    .querySelectorAll(".tipo-btn")
    .forEach(botao => {

        botao.addEventListener(
            "click",
            () => {

                grupo
                .querySelectorAll(".tipo-btn")
                .forEach(btn => {

                    btn.classList.remove(
                        "ativo"
                    );

                });

                botao.classList.add(
                    "ativo"
                );

                input.value =
                    botao.dataset.tipo;

            }
        );

    });

});

