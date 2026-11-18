(function () {

    // Proteção contra carregamento duplicado: se este arquivo for
    // incluído mais de uma vez na página (por exemplo, no base.html e
    // de novo no bloco de scripts da página), os cliques seriam
    // registrados em duplicidade. Só a primeira execução vale.
    if (window.__sigcModalIniciado) { return; }
    window.__sigcModalIniciado = true;

document.addEventListener(

    "DOMContentLoaded",

    () => {

        const openButtons =
            document.querySelectorAll("[data-modal]");

        const closeButtons =
            document.querySelectorAll("[data-close-modal]");

        openButtons.forEach(button => {

            button.addEventListener(

                "click",

                () => {

                    const modalId =
                        button.dataset.modal;

                    const modal =
                        document.getElementById(modalId);

                    if(modal){

                        modal.classList.add("active");

                    }

                }

            );

        });

        closeButtons.forEach(button => {

            button.addEventListener(

                "click",

                () => {

                    const modal =
                        button.closest(".modal");

                    if(modal){

                        modal.classList.remove("active");

                    }

                }

            );

        });

        document.querySelectorAll(".modal")
            .forEach(modal => {

                modal.addEventListener(

                    "click",

                    (e) => {

                        if(e.target === modal){

                            modal.classList.remove("active");

                        }

                    }

                );

            });

    }

);

})();