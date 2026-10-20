document.addEventListener('DOMContentLoaded', function () {

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

    var formulario = document.querySelector('.login-form');
    var botaoEntrar = document.getElementById('botao-entrar');

    if (formulario && botaoEntrar) {

        formulario.addEventListener('submit', function (evento) {
            if (!formulario.checkValidity()) { return; }
            botaoEntrar.classList.add('is-loading');
            botaoEntrar.disabled = true;
        });

    }

});