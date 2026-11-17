/* ============================================================
   SIGC — Flash messages (alertas)
   Mantém o contrato anterior: age sobre todos os elementos
   ".alert" presentes no DOMContentLoaded (gerados pelo Flask
   no base.html). Acrescenta, sem alterar o HTML do template:
   - contêiner que empilha vários alertas sem sobreposição;
   - botão de fechar manual (acessível);
   - fechamento automático (5s; 8s para erro/aviso), pausado
     enquanto o usuário passa o mouse, toca ou foca no alerta;
   - saída animada (a classe .alert-saindo + transição no CSS).
   ============================================================ */
   document.addEventListener("DOMContentLoaded", function () {

    var alertas = document.querySelectorAll(".alert");
    if (!alertas.length) { return; }

    var TEMPO_PADRAO = 5000;   /* success, info e demais */
    var TEMPO_ATENCAO = 8000;  /* error, danger, warning */
    var TEMPO_RETOMADA = 3000; /* após o usuário tirar o mouse/foco */
    var DURACAO_SAIDA = 500;   /* igual ao tempo antes usado para remover */

    var pilha = document.createElement("div");
    pilha.className = "alert-stack";
    pilha.setAttribute("aria-live", "polite");
    document.body.appendChild(pilha);

    function categoria(alerta) {
        var m = alerta.className.match(/alert-(success|error|danger|warning|info)/);
        return m ? m[1] : "info";
    }

    function remover(alerta) {
        if (alerta.dataset.fechando === "1") { return; }
        alerta.dataset.fechando = "1";
        alerta.classList.add("alert-saindo");
        setTimeout(function () {
            alerta.remove();
            if (!pilha.children.length) { pilha.remove(); }
        }, DURACAO_SAIDA);
    }

    alertas.forEach(function (alerta) {

        var tipo = categoria(alerta);
        var atencao = (tipo === "error" || tipo === "danger" || tipo === "warning");

        alerta.setAttribute("role", atencao ? "alert" : "status");

        /* Botão de fechar manual */
        var botao = document.createElement("button");
        botao.type = "button";
        botao.className = "alert-close";
        botao.setAttribute("aria-label", "Fechar mensagem");
        botao.innerHTML = '<i class="fa-solid fa-xmark" aria-hidden="true"></i>';
        botao.addEventListener("click", function () { remover(alerta); });
        alerta.appendChild(botao);

        pilha.appendChild(alerta);

        /* Fechamento automático com pausa */
        var timer = null;
        function agendar(ms) {
            clearTimeout(timer);
            timer = setTimeout(function () { remover(alerta); }, ms);
        }
        function pausar() { clearTimeout(timer); }

        alerta.addEventListener("mouseenter", pausar);
        alerta.addEventListener("focusin", pausar);
        alerta.addEventListener("touchstart", pausar, { passive: true });
        alerta.addEventListener("mouseleave", function () { agendar(TEMPO_RETOMADA); });
        alerta.addEventListener("focusout", function () { agendar(TEMPO_RETOMADA); });

        agendar(atencao ? TEMPO_ATENCAO : TEMPO_PADRAO);
    });
});