// Campo de pesquisa
document
.getElementById("search-input")
.addEventListener(
    "keyup",
    function(){

        // Texto digitado
        let filtro =
            this.value.toLowerCase();

        // Todas as linhas da tabela
        let linhas =
            document.querySelectorAll(
                ".linha-movimentacao"
            );

        // Percorre cada linha
        linhas.forEach(

            function(linha){

                // Pega o nome do produto
                let produto =
                    linha
                    .querySelector(".produto")
                    .innerText
                    .toLowerCase();

                // Se encontrou o texto digitado
                if(
                    produto.includes(filtro)
                ){

                    // Mostra a linha
                    linha.style.display = "";

                }

                else{

                    // Esconde a linha
                    linha.style.display = "none";

                }

            }

        );

    }

);