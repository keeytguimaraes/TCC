// ========================================
// ABRIR MODAL DE DESATIVAÇÃO
// ========================================
function abrirModalDesativar(
    clienteId,
    clienteNome,
    contaAberta,
    saldo
){

    console.log("BOTÃO DESATIVAR CLICADO");

    const modal = document.getElementById(
        "modalDesativar"
    );

    const conteudo = document.getElementById(
        "conteudo-modal"
    );

    const form = document.getElementById(
        "formDesativarCliente"
    );

    const btnDesativar = document.getElementById(
        "btnDesativarCliente"
    );

    // Verificações para descobrir erros
    console.log("Modal:", modal);
    console.log("Conteúdo:", conteudo);
    console.log("Form:", form);
    console.log("Botão:", btnDesativar);

    if(
        !modal ||
        !conteudo ||
        !form ||
        !btnDesativar
    ){
        console.error(
            "Algum elemento do modal não foi encontrado."
        );
        return;
    }

    // ========================================
    // CLIENTE POSSUI CONTA ABERTA
    // ========================================
    if(
        contaAberta === "True" ||
        contaAberta === true ||
        contaAberta == 1
    ){

        conteudo.innerHTML = `
            <div class="alerta-conta-aberta">

                <h3>
                    ⚠ Cliente possui conta em aberto
                </h3>

                <p>
                    <strong>Cliente:</strong>
                    ${clienteNome}
                </p>

                <p>
                    <strong>Saldo devedor:</strong>
                    R$ ${saldo}
                </p>

                <p class="texto-aviso">
                    Este cliente não poderá ser desativado
                    até que a conta seja quitada.
                </p>

            </div>
        `;

        btnDesativar.style.display =
            "none";

    }

    // ========================================
    // CLIENTE SEM CONTA ABERTA
    // ========================================
    else{

        conteudo.innerHTML = `
            <p>
                Deseja realmente desativar o cliente
                <strong>${clienteNome}</strong>?
            </p>

            <p class="texto-aviso">
                O cliente deixará de aparecer
                na listagem.
            </p>
        `;

        btnDesativar.style.display =
            "inline-block";

        form.action =
            "/cliente/desativar/" +
            clienteId;
    }

    modal.classList.add(
        "ativo"
    );
}

// ========================================
// FECHAR MODAL
// ========================================
function fecharModalExcluir(){

    const modal =
        document.getElementById(
            "modalDesativar"
        );

    if(modal){

        modal.classList.remove(
            "ativo"
        );

    }

}

// ========================================
// FECHAR AO CLICAR FORA
// ========================================
window.addEventListener(
    "click",
    function(event){

        const modal =
            document.getElementById(
                "modalDesativar"
            );

        if(
            modal &&
            event.target === modal
        ){

            fecharModalExcluir();

        }

    }
);