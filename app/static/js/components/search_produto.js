document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("search-input");
    const contador = document.getElementById("search-count");
    const vazio = document.getElementById("search-empty");

    if (!input) return;

    const itens = document.querySelectorAll(".search-item");

    function normalizarTexto(texto){

        return texto
            .toLowerCase()
            .normalize("NFD")
            .replace(/[̀-ͯ]/g, "");

    }

    function atualizarPesquisa(){

        const pesquisa = normalizarTexto(
            input.value
        );

        let encontrados = 0;

        itens.forEach(item => {

            const alvo = item.querySelector(
                ".search-text"
            );

            const texto = normalizarTexto(
                alvo ? alvo.textContent : ""
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

        // ESTADO VAZIO DA PESQUISA

        if(vazio){

            vazio.hidden = !(
                pesquisa !== "" &&
                encontrados === 0
            );

        }

    }

    input.addEventListener(
        "input",
        atualizarPesquisa
    );

    atualizarPesquisa();

});