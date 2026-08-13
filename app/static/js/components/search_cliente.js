document.addEventListener("DOMContentLoaded", () => {

    const input = document.getElementById("search-input");
    const contador = document.getElementById("search-count");
    const cardCadastro = document.getElementById("card-cadastro");
    const campoNome = document.getElementById("nome-cliente");
    const searchEmpty = document.getElementById("search-empty");

    if (!input) return;

    const itens = document.querySelectorAll(".search-item");

    function normalizarTexto(texto){

        return texto
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

    }

    function atualizarPesquisa(){

        const pesquisa = normalizarTexto(input.value);

        let encontrados = 0;

        itens.forEach(item => {

            const texto = normalizarTexto(
                item.querySelector(".search-text").textContent
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

                    contador.textContent = "1 cliente";

                }else{

                    contador.textContent = `${itens.length} clientes`;

                }

            }else if(encontrados === 0){

                contador.textContent = "Nenhum cliente encontrado.";

            }else if(encontrados === 1){

                contador.textContent = "1 cliente encontrado.";

            }else{

                contador.textContent = `${encontrados} clientes encontrados.`;

            }

        }

        // CARD "NENHUM CLIENTE ENCONTRADO"
        if(searchEmpty){

            if(pesquisa !== "" && encontrados === 0){

                searchEmpty.classList.remove("search-hidden");

            }else{

                searchEmpty.classList.add("search-hidden");

            }

        }

        // CARD DE CADASTRO
        if(cardCadastro){

            if(pesquisa === ""){

                cardCadastro.classList.remove("hidden");

            }else{

                cardCadastro.classList.add("hidden");

            }

        }

    }

    input.addEventListener("input", atualizarPesquisa);

    input.addEventListener("keydown", function(e){

        if(e.key === "Enter"){

            const pesquisa = normalizarTexto(input.value);

            let encontrou = false;

            itens.forEach(item => {

                const texto = normalizarTexto(
                    item.querySelector(".search-text").textContent
                );

                if(texto.includes(pesquisa)){

                    encontrou = true;

                }

            });

            if(!encontrou && pesquisa !== ""){

                e.preventDefault();

                input.value = "";

                atualizarPesquisa();

                if(campoNome){

                    campoNome.focus();

                }

            }

        }

    });

    // ==========================
    // BOTÃO CADASTRAR CLIENTE
    // ==========================

    const btnCadastrar = document.getElementById(
        "btn-cadastrar-cliente"
    );

    if(btnCadastrar && cardCadastro){

        btnCadastrar.addEventListener(
            "click",
            () => {

                input.value = "";

                atualizarPesquisa();

                cardCadastro.scrollIntoView({

                    behavior: "smooth",

                    block: "center"

                });

                if(campoNome){

                    campoNome.focus();

                }

            }
        );

    }

    atualizarPesquisa();

});