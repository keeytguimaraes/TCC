document.addEventListener("DOMContentLoaded", () => {

    const senha =
        document.getElementById("senha");

    const confirmar =
        document.getElementById(
            "confirmar_senha"
        );

    document
        .getElementById("toggle-senha")
        ?.addEventListener("click", () => {

            senha.type =
                senha.type === "password"
                ? "text"
                : "password";

        });

    document
        .getElementById("toggle-confirmar")
        ?.addEventListener("click", () => {

            confirmar.type =
                confirmar.type === "password"
                ? "text"
                : "password";

        });

});