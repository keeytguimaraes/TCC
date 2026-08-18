document
.getElementById("search-input")
.addEventListener(

    "keyup",

    function(){

        let filtro =
            this.value.toLowerCase();

        let cards =
            document.querySelectorAll(
                ".estoque-card"
            );

        cards.forEach(

            function(card){

                let nome =
                    card
                    .querySelector("h3")
                    .innerText
                    .toLowerCase();

                if(
                    nome.includes(
                        filtro
                    )
                ){

                    card.style.display =
                        "block";

                }

                else{

                    card.style.display =
                        "none";

                }

            }

        );

    }

);

const botoes =
    document.querySelectorAll(".filtro-btn");

botoes.forEach(

    function(botao){

        botao.addEventListener(

            "click",

            function(){

                const status =
                    this.dataset.status;

                const cards =
                    document.querySelectorAll(
                        ".estoque-card"
                    );

                cards.forEach(

                    function(card){

                        if(
                            status === "todos"
                        ){

                            card.style.display =
                                "block";

                        }

                        else if(
                            card.dataset.status
                            === status
                        ){

                            card.style.display =
                                "block";

                        }

                        else{

                            card.style.display =
                                "none";

                        }

                    }

                );

            }

        );

    }

);