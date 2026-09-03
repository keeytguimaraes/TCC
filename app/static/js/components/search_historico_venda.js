const campoPesquisa =
    document.getElementById(
        "search-input"
    );

const linhas =
    document.querySelectorAll(
        ".linha-venda"
    );

campoPesquisa.addEventListener(
    "keyup",

    function(){

        const termo =
            this.value.toLowerCase();

        linhas.forEach(function(linha){

            const texto =
                linha.textContent.toLowerCase();

            if(
                texto.includes(termo)
            ){

                linha.style.display =
                    "";

            }
            else{

                linha.style.display =
                    "none";

            }

        });

    }
);