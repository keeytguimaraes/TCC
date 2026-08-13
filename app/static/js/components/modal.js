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