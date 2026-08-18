document.addEventListener("DOMContentLoaded", () => {

    const input =
        document.getElementById(
            "search-input"
        );

    const contador =
        document.getElementById(
            "search-count"
        );

    const searchEmpty =
        document.getElementById(
            "search-empty"
        );

    if(!input) return;

    const itens =
        document.querySelectorAll(
            ".search-item"
        );

    function normalizarTexto(texto){

        return texto
            .toLowerCase()
            .normalize("NFD")
            .replace(
                /[\u0300-\u036f]/g,
                ""
            );

    }

    function atualizarPesquisa(){

        const pesquisa =
            normalizarTexto(
                input.value
            );

        let encontrados = 0;

        itens.forEach(item => {

            const texto =
                normalizarTexto(
                    item.querySelector(
                        ".search-text"
                    ).textContent
                );

            if(
                texto.includes(
                    pesquisa
                )
            ){

                item.style.display = "";

                encontrados++;

            }else{

                item.style.display =
                    "none";

            }

        });

        if(contador){

            if(
                pesquisa === ""
            ){

                contador.textContent =
                    `${itens.length} fiado(s)`;

            }else{

                contador.textContent =
                    `${encontrados} encontrado(s)`;

            }

        }

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

    }

    input.addEventListener(
        "input",
        atualizarPesquisa
    );

    atualizarPesquisa();

});