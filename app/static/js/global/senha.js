document.addEventListener("DOMContentLoaded", () => {

    // Proteção contra carregamento duplicado.
    //
    // O base.html já carrega este arquivo em todas as páginas que
    // herdam dele. Quando a própria página (por exemplo, cadastrar
    // usuário) o carrega de novo, o clique ficaria registrado duas
    // vezes: o campo mudaria para "text" e voltaria para "password"
    // no mesmo clique, e a senha nunca apareceria. Só a primeira
    // execução vale.
    if (window.__sigcSenhaIniciado) {
        return;
    }

    window.__sigcSenhaIniciado = true;

    // Liga o botão de olho ao campo de senha correspondente.
    function configurarOlho(idBotao, idCampo) {

        const botao =
            document.getElementById(idBotao);

        const campo =
            document.getElementById(idCampo);

        if (!botao || !campo) {
            return;
        }

        botao.addEventListener("click", () => {

            const mostrar =
                campo.type === "password";

            campo.type =
                mostrar
                ? "text"
                : "password";

            botao.setAttribute(
                "aria-pressed",
                String(mostrar)
            );

            // O ícone acompanha o estado da senha:
            // olho aberto = senha oculta; olho riscado = senha visível.
            const icone =
                botao.querySelector("i");

            if (icone) {
                icone.classList.toggle("fa-eye", !mostrar);
                icone.classList.toggle("fa-eye-slash", mostrar);
            }

        });

    }

    configurarOlho("toggle-senha", "senha");

    configurarOlho("toggle-confirmar", "confirmar_senha");

});