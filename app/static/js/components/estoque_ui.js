document.addEventListener('DOMContentLoaded', function () {

    // Acessibilidade: permite ativar por teclado (Enter/Espaço)
    // elementos que funcionam como botão/link mas não são <button>/<a> nativos.
    // Não interfere em nenhuma lógica de clique já existente — apenas
    // simula o clique quando o elemento está focado via teclado.
    function ativarPorTeclado(selector) {
        document.querySelectorAll(selector).forEach(function (el) {
            el.addEventListener('keydown', function (e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    el.click();
                }
            });
        });
    }

    ativarPorTeclado('.nova-entrada-card[role="button"]');
    ativarPorTeclado('.estoque-card[role="link"]');

    // Estado visual do filtro ativo.
    // Apenas adiciona/remove a classe "is-active" para feedback visual.
    // Não interfere na lógica de filtragem em si (que continua em
    // search_estoque.js, lendo o mesmo atributo data-status de sempre).
    var filtros = document.querySelectorAll('.filtro-btn');

    filtros.forEach(function (btn) {
        btn.addEventListener('click', function () {
            filtros.forEach(function (b) {
                b.classList.remove('is-active');
            });
            btn.classList.add('is-active');
        });
    });

});