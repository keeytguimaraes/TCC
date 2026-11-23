/* ==========================================================
   DESEMPENHO DE FUNCIONÁRIOS — SIGC
   Página: relatorio/desempenho_funcionarios.html

   - Atalhos de período (Hoje, Últimos 7 dias, Este mês, Mês anterior).
   - Validação: a data final não pode ser anterior à inicial.
   - Período inicial: mês atual.
   ========================================================== */

   (function () {
    "use strict";

    var form = document.getElementById("rl-form-desempenho");
    if (!form) { return; }

    var inicial = document.getElementById("rl-data-inicial");
    var final = document.getElementById("rl-data-final");
    var aviso = document.getElementById("rd-aviso-data");
    var atalhos = form.querySelectorAll(".rd-atalho");

    // Data local no formato AAAA-MM-DD (sem passar por UTC).
    function formatar(data) {
        var mes = String(data.getMonth() + 1).padStart(2, "0");
        var dia = String(data.getDate()).padStart(2, "0");
        return data.getFullYear() + "-" + mes + "-" + dia;
    }

    function calcular(periodo) {
        var hoje = new Date();
        var ano = hoje.getFullYear();
        var mes = hoje.getMonth();

        if (periodo === "hoje") {
            return [hoje, hoje];
        }
        if (periodo === "7dias") {
            return [new Date(ano, mes, hoje.getDate() - 6), hoje];
        }
        if (periodo === "mes") {
            return [new Date(ano, mes, 1), hoje];
        }
        if (periodo === "mes-anterior") {
            return [new Date(ano, mes - 1, 1), new Date(ano, mes, 0)];
        }
        return null;
    }

    function validar() {
        var invalido = inicial.value && final.value && final.value < inicial.value;

        final.setCustomValidity(
            invalido ? "A data final não pode ser anterior à data inicial." : ""
        );
        aviso.hidden = !invalido;

        return !invalido;
    }

    function marcarAtalho(periodo) {
        atalhos.forEach(function (botao) {
            var ativo = botao.getAttribute("data-periodo") === periodo;
            botao.classList.toggle("rd-atalho--ativo", ativo);
            botao.setAttribute("aria-pressed", ativo ? "true" : "false");
        });
    }

    atalhos.forEach(function (botao) {
        botao.setAttribute("aria-pressed", "false");

        botao.addEventListener("click", function () {
            var periodo = botao.getAttribute("data-periodo");
            var intervalo = calcular(periodo);

            if (!intervalo) { return; }

            inicial.value = formatar(intervalo[0]);
            final.value = formatar(intervalo[1]);
            validar();
            marcarAtalho(periodo);
        });
    });

    // Digitar as datas manualmente desmarca o atalho.
    [inicial, final].forEach(function (campo) {
        campo.addEventListener("input", function () {
            validar();
            marcarAtalho(null);
        });
    });

    form.addEventListener("submit", function (evento) {
        if (!validar()) {
            evento.preventDefault();
            final.reportValidity();
        }
    });

    // Período inicial: mês atual.
    var padrao = calcular("mes");
    inicial.value = formatar(padrao[0]);
    final.value = formatar(padrao[1]);
    marcarAtalho("mes");
})();