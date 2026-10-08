document.addEventListener('DOMContentLoaded', function () {

    // Mostrar/ocultar senha
    var botaoToggle = document.getElementById('toggle-senha');
    var campoSenha = document.getElementById('senha');

    if (botaoToggle && campoSenha) {

        botaoToggle.addEventListener('click', function () {

            var visivel = botaoToggle.classList.toggle('is-visible');

            campoSenha.type = visivel ? 'text' : 'password';
            botaoToggle.setAttribute('aria-pressed', String(visivel));
            botaoToggle.setAttribute(
            'aria-label',
            visivel ? 'Ocultar senha' : 'Mostrar senha'
        );

    });

}

    // Estado de carregamento no botao ao submeter o formulario.
    // O formulario continua submetendo normalmente para o Flask -
    // isto so da feedback visual enquanto a resposta nao chega.
    var formulario = document.querySelector('.login-form');
    var botaoEntrar = document.getElementById('botao-entrar');

    if (formulario && botaoEntrar) {

        formulario.addEventListener('submit', function (evento) {

            if (!formulario.checkValidity()) {
                return;
            }

            botaoEntrar.classList.add('is-loading');
            botaoEntrar.disabled = true;

        });

    }

});