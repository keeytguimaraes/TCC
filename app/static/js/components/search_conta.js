document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById(
        "search-input"
    );

    if (!input) return;

    const cards = document.querySelectorAll(
        ".conta-card"
    );

    function normalizar(texto){

        return texto
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

    }

    function pesquisar(){

        const termo = normalizar(
            input.value
        );

        cards.forEach(card => {

            const nome = normalizar(

                card.querySelector(
                    ".cliente-nome"
                ).textContent

            );

            if(nome.includes(termo)){

                card.style.display = "";

            }else{

                card.style.display = "none";

            }

        });

    }

    input.addEventListener(
        "input",
        pesquisar
    );

});