document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("search-input");
    const contador = document.getElementById("search-count");
    const cardNovoProduto = document.querySelector(".novo-produto-card");

    if (!input) return;

    const itens = document.querySelectorAll(".search-item");

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

        // CONTADOR

        if(contador){

            if(pesquisa === ""){

                if(itens.length === 1){

                    contador.textContent =
                        "1 produto";

                }else{

                    contador.textContent =
                        `${itens.length} produtos`;

                }

            }else if(encontrados === 0){

                contador.textContent =
                    "Nenhum produto encontrado.";

            }else if(encontrados === 1){

                contador.textContent =
                    "1 produto encontrado.";

            }else{

                contador.textContent =
                    `${encontrados} produtos encontrados.`;

            }

        }

        // CARD NOVO PRODUTO

        if(cardNovoProduto){

            if(pesquisa === ""){

                cardNovoProduto.style.display = "flex";

            }else{

                cardNovoProduto.style.display = "none";

            }

        }

    }

    input.addEventListener(
        "input",
        atualizarPesquisa
    );

    atualizarPesquisa();

});