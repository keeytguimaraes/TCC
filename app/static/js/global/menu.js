document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.querySelector(".sidebar");

    const btnToggle = document.querySelector(".header-toggle");

    if (!sidebar || !btnToggle) return;

    // Recupera estado salvo
    if (
        localStorage.getItem("menu-fechado")
        === "true"
    ) {

        sidebar.classList.add("recolhido");

    }

    btnToggle.addEventListener("click", () => {

        sidebar.classList.toggle(
            "recolhido"
        );

        localStorage.setItem(
            "menu-fechado",
            sidebar.classList.contains(
                "recolhido"
            )
        );

    });

});