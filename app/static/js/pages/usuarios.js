document.addEventListener("DOMContentLoaded", () => {
    // Encontra a barra de pesquisa da página atual.
    const pesquisa = document.querySelector("[data-busca-usuarios]");

    // Encontra a lista que pertence a essa barra de pesquisa.
    const lista = document.querySelector("[data-lista-usuarios]");

    // Encontra os elementos usados para exibir a contagem
    // e a mensagem de pesquisa sem resultados.
    const contagem = document.querySelector("[data-contagem-usuarios]");
    const mensagemVazia = document.querySelector("[data-vazio-busca]");

    // Se a página não tiver esses elementos, encerra a execução.
    if (!pesquisa || !lista) {
        return;
    }

    // Guarda os cards existentes nessa lista.
    const itens = Array.from(lista.querySelectorAll("[data-item-usuario]"));

    // A contagem representa os itens visíveis após a pesquisa.
    function atualizarPesquisa() {
        const termo = pesquisa.value
            .trim()
            .toLocaleLowerCase("pt-BR");

        let quantidadeVisivel = 0;

        itens.forEach((item) => {
            // Usa data-busca (nome, login e perfil) quando existir, para que
            // os textos dos botões ("Editar", "Senha"...) não entrem na busca.
            const texto = (item.dataset.busca || item.textContent)
                .toLocaleLowerCase("pt-BR");

            const corresponde = texto.includes(termo);

            item.hidden = !corresponde;

            if (corresponde) {
                quantidadeVisivel++;
            }
        });

        if (contagem) {
            contagem.textContent =
                `${quantidadeVisivel} usuário(s)`;
        }

        // A mensagem só aparece quando existe uma pesquisa
        // e nenhum card corresponde ao texto informado.
        if (mensagemVazia) {
            mensagemVazia.hidden =
                termo.length === 0 || quantidadeVisivel > 0;
        }
    }

    // Atualiza os resultados enquanto o usuário digita.
    pesquisa.addEventListener("input", atualizarPesquisa);
});