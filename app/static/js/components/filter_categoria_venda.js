// ==========================
// FILTRO POR CATEGORIA
// ==========================

const botoesCategoria =
    document.querySelectorAll(
        ".categoria-btn"
    );

botoesCategoria.forEach(botao => {

    botao.addEventListener(
        "click",
        function () {

            // Remove ativo
            botoesCategoria.forEach(btn => {

                btn.classList.remove(
                    "active"
                );

            });

            // Ativa atual
            this.classList.add(
                "active"
            );

            // Categoria clicada
            const categoria =
                this.dataset.categoria;

            // Cards
            const cards =
                document.querySelectorAll(
                    ".produto-card"
                );

            cards.forEach(card => {

                const categoriaProduto =
                    card.dataset.categoria;

                // Mostrar todos
                if (
                    categoria === ""
                ) {

                    card.style.display =
                        "flex";

                    return;
                }

                // Mostrar apenas categoria
                if (
                    categoriaProduto === categoria
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

});