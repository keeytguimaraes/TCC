// ==========================
// FILTRO DE PRODUTOS
// ==========================

const categoriaSelect =
    document.getElementById(
        "categoria"
    );

const produtoSelect =
    document.getElementById(
        "produto"
    );

if (
    categoriaSelect &&
    produtoSelect
) {

    categoriaSelect.addEventListener(
        "change",

        function () {

            const categoria =
                this.value;

            const produtos =
                produtoSelect.options;

            for (
                let i = 0;
                i < produtos.length;
                i++
            ) {

                const categoriaProduto =
                    produtos[i].getAttribute(
                        "data-categoria"
                    );

                if (i === 0) {

                    produtos[i].style.display =
                        "block";

                    continue;
                }

                if (
                    categoriaProduto === categoria
                ) {

                    produtos[i].style.display =
                        "block";
                }

                else {

                    produtos[i].style.display =
                        "none";
                }
            }

            produtoSelect.value = "";
        }
    );
}


// ==========================
// ORIGEM DA COMPRA
// ==========================

const origemCompra =
    document.getElementById(
        "origem_compra"
    );

const fornecedorGroup =
    document.getElementById(
        "fornecedor-group"
    );

const localGroup =
    document.getElementById(
        "local-group"
    );

function atualizarOrigemCompra() {

    if (
        !origemCompra
    ) {
        return;
    }

    if (
        origemCompra.value == "1"
    ) {

        fornecedorGroup.style.display =
            "block";

        localGroup.style.display =
            "none";
    }

    else {

        fornecedorGroup.style.display =
            "none";

        localGroup.style.display =
            "block";
    }
}

if (origemCompra) {

    origemCompra.addEventListener(
        "change",
        atualizarOrigemCompra
    );

    atualizarOrigemCompra();
}

const form = document.querySelector("form");

form.addEventListener("submit", function(e){

    const caixas = parseInt(
        document.querySelector(
            '[name="quantidade_recebida_caixa"]'
        ).value
    ) || 0;

    const unidades = parseInt(
        document.querySelector(
            '[name="quantidade_recebida_unidade"]'
        ).value
    ) || 0;

    if(caixas === 0 && unidades === 0){

        e.preventDefault();

        alert(
            "Informe ao menos caixas ou unidades."
        );

    }

});