// ==========================
// PESQUISA DE PRODUTOS
// ==========================

const pesquisaProduto =
    document.getElementById(
        "pesquisa-produto"
    );

if (pesquisaProduto) {

    pesquisaProduto.addEventListener(
        "keyup",
        function () {

            const texto =
                this.value
                    .toLowerCase()
                    .trim();

            const cards =
                document.querySelectorAll(
                    ".produto-card"
                );

            cards.forEach(card => {

                const nome =
                    card.querySelector(
                        "h3"
                    )
                    .textContent
                    .toLowerCase();

                if (
                    nome.includes(texto)
                ) {

                    card.style.display =
                        "flex";
                }

                else {

                    card.style.display =
                        "none";
                }

            });

        }
    );

}