document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById(
        "search-input"
    );

    const contador = document.getElementById(
        "search-count"
    );

    const searchEmpty = document.getElementById(
        "search-empty"
    );

    const cardCadastro = document.getElementById(
        "card-cadastro"
    );

    if (!input) return;

    const itens = document.querySelectorAll(
        ".search-item"
    );

    function normalizarTexto(texto){

        return texto
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

    }

    function atualizarPesquisa(){

        const pesquisa = normalizarTexto(
            input.value
        );

        let encontrados = 0;

        itens.forEach(item => {

            const texto = normalizarTexto(
                item.querySelector(
                    ".search-text"
                ).textContent
            );

            if(texto.includes(pesquisa)){

                item.style.display = "";
                encontrados++;

            }else{

                item.style.display = "none";

            }

        });

        // ==========================
        // CONTADOR
        // ==========================

        if(contador){

            if(pesquisa === ""){

                if(itens.length === 1){

                    contador.textContent =
                        "1 fornecedor";

                }else{

                    contador.textContent =
                        `${itens.length} fornecedores`;

                }

            }else if(encontrados === 0){

                contador.textContent ="";

            }else if(encontrados === 1){

                contador.textContent =
                    "1 fornecedor encontrado.";

            }else{

                contador.textContent =
                    `${encontrados} fornecedores encontrados.`;

            }

        }

        // ==========================
        // CARD "NENHUM ENCONTRADO"
        // ==========================

        if(searchEmpty){

            if(
                pesquisa !== "" &&
                encontrados === 0
            ){

                searchEmpty.classList.remove(
                    "search-hidden"
                );

            }else{

                searchEmpty.classList.add(
                    "search-hidden"
                );

            }

        }

        // ==========================
        // CARD NOVO FORNECEDOR
        // ==========================

        if(cardCadastro){

            if(pesquisa === ""){

                cardCadastro.style.display = "";

            }else{

                cardCadastro.style.display = "none";

            }

        }

    }

    input.addEventListener(
        "input",
        atualizarPesquisa
    );

    atualizarPesquisa();

});