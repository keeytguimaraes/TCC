/* ==========================================================
   RELATÓRIOS — SIGC
   Páginas: Fechamento Diário e Relatório de Vendas.

   - Atalhos de seleção de datas.
   - Preenchimento automático dos períodos.
   - Validação das datas.
   - Destaque visual do atalho selecionado.
   - Datas calculadas no horário local.
   ========================================================== */

   (function () {
    "use strict";

    var formularios = document.querySelectorAll(
        "[data-relatorio-periodo]"
    );

    if (!formularios.length) return;

    // Formata uma data no padrão AAAA-MM-DD.
    function formatar(data) {
        var mes = String(data.getMonth() + 1).padStart(2, "0");
        var dia = String(data.getDate()).padStart(2, "0");

        return data.getFullYear() + "-" + mes + "-" + dia;
    }

    // Calcula os intervalos de período.
    function calcularPeriodo(periodo) {
        var hoje = new Date();
        var ano = hoje.getFullYear();
        var mes = hoje.getMonth();

        switch (periodo) {

            case "hoje":
                return [hoje, hoje];

            case "ontem":
                return [
                    new Date(ano, mes, hoje.getDate() - 1),
                    new Date(ano, mes, hoje.getDate() - 1)
                ];

            case "7dias":
                return [
                    new Date(ano, mes, hoje.getDate() - 6),
                    hoje
                ];

            case "mes":
                return [
                    new Date(ano, mes, 1),
                    hoje
                ];

            case "mes-anterior":
                return [
                    new Date(ano, mes - 1, 1),
                    new Date(ano, mes, 0)
                ];

            case "inicio-mes":
                return [
                    new Date(ano, mes, 1),
                    new Date(ano, mes, 1)
                ];

            case "fim-mes":
                return [
                    new Date(ano, mes + 1, 0),
                    new Date(ano, mes + 1, 0)
                ];

            default:
                return null;
        }
    }

    formularios.forEach(function (form) {

        var modo = form.dataset.modo;

        var dataUnica = form.querySelector("#rl-data");
        var inicial = form.querySelector("#rl-data-inicial");
        var final = form.querySelector("#rl-data-final");

        var aviso = form.querySelector(".ra-aviso-data");
        var atalhos = form.querySelectorAll(".ra-atalho");

        // Ativa visualmente o atalho selecionado.
        function marcarAtalho(periodo) {

            atalhos.forEach(function (botao) {

                var ativo =
                    botao.dataset.periodo === periodo;

                botao.classList.toggle(
                    "ra-atalho--ativo",
                    ativo
                );

                botao.setAttribute(
                    "aria-pressed",
                    ativo ? "true" : "false"
                );
            });
        }

        // Validação exclusiva para formulários com intervalo.
        function validar() {

            if (modo !== "periodo") return true;

            var invalido =
                inicial.value &&
                final.value &&
                final.value < inicial.value;

            final.setCustomValidity(
                invalido
                    ? "A data final não pode ser anterior à data inicial."
                    : ""
            );

            if (aviso) {
                aviso.hidden = !invalido;
            }

            return !invalido;
        }

        atalhos.forEach(function (botao) {

            botao.setAttribute("aria-pressed", "false");

            botao.addEventListener("click", function () {

                var periodo = botao.dataset.periodo;
                var intervalo = calcularPeriodo(periodo);

                if (!intervalo) return;

                if (modo === "dia" && dataUnica) {

                    dataUnica.value = formatar(intervalo[0]);

                } else if (modo === "periodo" && inicial && final) {

                    inicial.value = formatar(intervalo[0]);
                    final.value = formatar(intervalo[1]);

                    validar();
                }

                marcarAtalho(periodo);
            });
        });

        // Alterações manuais retiram o destaque do atalho.
        if (modo === "dia" && dataUnica) {

            dataUnica.addEventListener("input", function () {
                marcarAtalho(null);
            });

        } else if (modo === "periodo" && inicial && final) {

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
        }

        // Define os valores iniciais.
        if (modo === "dia" && dataUnica) {

            var hoje = formatar(new Date());

            dataUnica.value = hoje;
            marcarAtalho("hoje");

        } else if (modo === "periodo" && inicial && final) {

            var padrao = calcularPeriodo("mes");

            inicial.value = formatar(padrao[0]);
            final.value = formatar(padrao[1]);

            marcarAtalho("mes");
        }

    });

})();