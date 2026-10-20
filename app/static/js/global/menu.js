(function () {
    "use strict";

    var sidebar = document.querySelector(".sidebar");
    var btnToggle = document.querySelector(".header-toggle");

    if (!sidebar || !btnToggle) {
        return;
    }

    var MEDIA_DESKTOP = window.matchMedia("(min-width: 1025px)");

    // aria-controls precisa de um id — atribuído em runtime,
    // sem exigir alteração no HTML.
    if (!sidebar.id) {
        sidebar.id = "sidebar-principal";
    }
    btnToggle.setAttribute("aria-controls", sidebar.id);
    if (!btnToggle.hasAttribute("aria-label")) {
        btnToggle.setAttribute("aria-label", "Abrir ou fechar menu");
    }

    // Overlay da gaveta mobile — criado em runtime, não exige
    // alteração em menu.html/base.html.
    var overlay = document.createElement("div");
    overlay.className = "sidebar-overlay";
    document.body.appendChild(overlay);

    function isDesktop() {
        return MEDIA_DESKTOP.matches;
    }

    function sincronizarAria() {
        var ativo = sidebar.classList.contains("recolhido");
        // Desktop: "recolhido" = encolhida. Mobile: "recolhido" = gaveta aberta.
        var expandida = isDesktop() ? !ativo : ativo;
        btnToggle.setAttribute("aria-expanded", String(expandida));
    }

    function abrirGaveta() {
        sidebar.classList.add("recolhido");
        overlay.classList.add("is-visible");
        document.body.classList.add("menu-aberto");
        sincronizarAria();
    }

    function fecharGaveta() {
        sidebar.classList.remove("recolhido");
        overlay.classList.remove("is-visible");
        document.body.classList.remove("menu-aberto");
        sincronizarAria();
    }

    function alternarDesktop() {
        var colapsada = sidebar.classList.toggle("recolhido");
        localStorage.setItem("menu-fechado", colapsada);
        sincronizarAria();
    }

    btnToggle.addEventListener("click", function () {
        if (isDesktop()) {
            alternarDesktop();
        } else if (sidebar.classList.contains("recolhido")) {
            fecharGaveta();
        } else {
            abrirGaveta();
        }
    });

    overlay.addEventListener("click", fecharGaveta);

    document.addEventListener("keydown", function (evento) {
        if (evento.key === "Escape" && !isDesktop() && sidebar.classList.contains("recolhido")) {
            fecharGaveta();
            btnToggle.focus();
        }
    });

    // Troca de breakpoint em tempo real (ex: girar o tablet) não deixa
    // a gaveta "presa" aberta nem o desktop com estado conflitante.
    MEDIA_DESKTOP.addEventListener("change", function () {
        overlay.classList.remove("is-visible");
        document.body.classList.remove("menu-aberto");

        if (isDesktop()) {
            sidebar.classList.toggle("recolhido", localStorage.getItem("menu-fechado") === "true");
        } else {
            sidebar.classList.remove("recolhido");
        }
        sincronizarAria();
    });

    sincronizarAria();

})();