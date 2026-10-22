/* ==========================================================
   DASHBOARD — saudação dinâmica
   ----------------------------------------------------------
   Faixas de horário (fuso America/Sao_Paulo):
     05:00 – 11:59  -> Bom dia
     12:00 – 17:59  -> Boa tarde
     18:00 – 04:59  -> Boa noite
   O nome do usuário vem do Jinja (session["nome"]); aqui só
   são definidos o texto da saudação, o ícone, o período e a
   data. Sem JavaScript, o template exibe "Olá, <nome>".
   ========================================================== */
   (function () {
    "use strict";

    var TIMEZONE = "America/Sao_Paulo";

    var boasVindas = document.querySelector(".dashboard-boasvindas");
    if (!boasVindas) { return; }

    // Hora atual no fuso do Brasil; se Intl não estiver disponível,
    // usa o relógio do dispositivo.
    function horaAtual() {
        try {
            var partes = new Intl.DateTimeFormat("en-GB", {
                hour: "2-digit", hourCycle: "h23", timeZone: TIMEZONE
            }).format(new Date());
            var hora = parseInt(partes, 10);
            if (!isNaN(hora)) { return hora; }
        } catch (e) { /* usa o horário local abaixo */ }
        return new Date().getHours();
    }

    function periodo(hora) {
        if (hora >= 5 && hora < 12) { return { chave: "manha", texto: "Bom dia", icone: "fa-sun" }; }
        if (hora >= 12 && hora < 18) { return { chave: "tarde", texto: "Boa tarde", icone: "fa-cloud-sun" }; }
        return { chave: "noite", texto: "Boa noite", icone: "fa-moon" };
    }

    function dataPorExtenso() {
        try {
            var texto = new Intl.DateTimeFormat("pt-BR", {
                weekday: "long", day: "numeric", month: "long", timeZone: TIMEZONE
            }).format(new Date());
            return texto.charAt(0).toUpperCase() + texto.slice(1);
        } catch (e) { return ""; }
    }

    var p = periodo(horaAtual());

    var elTexto = boasVindas.querySelector("[data-saudacao]");
    var elIcone = boasVindas.querySelector("[data-saudacao-icone]");
    var elData = boasVindas.querySelector("[data-data-atual]");

    if (elTexto) { elTexto.textContent = p.texto; }

    if (elIcone) {
        elIcone.classList.remove("fa-sun", "fa-cloud-sun", "fa-moon");
        elIcone.classList.add(p.icone);
    }

    if (elData) { elData.textContent = dataPorExtenso(); }

    boasVindas.setAttribute("data-periodo", p.chave);
})();