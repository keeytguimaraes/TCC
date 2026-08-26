document.addEventListener(
    "DOMContentLoaded",
    () => {

        const checkboxDose =
            document.getElementById(
                "vende_por_dose"
            );

        const campoDose =
            document.getElementById(
                "campo-dose"
            );

        const campoPrecoDose =
            document.getElementById(
                "campo-preco-dose"
            );

        const checkboxUnidade =
            document.getElementById(
                "vende_por_unidade"
            );

        const campoPrecoUnidade =
            document.getElementById(
                "campo-preco-unidade"
            );

        function atualizarCampos() {

            if (
                checkboxDose
            ) {

                const mostrar =
                    checkboxDose.checked;

                if(campoDose)
                    campoDose.style.display =
                        mostrar
                        ? "block"
                        : "none";

                if(campoPrecoDose)
                    campoPrecoDose.style.display =
                        mostrar
                        ? "block"
                        : "none";
            }

            if (
                checkboxUnidade
            ) {

                const mostrar =
                    checkboxUnidade.checked;

                if(campoPrecoUnidade)
                    campoPrecoUnidade.style.display =
                        mostrar
                        ? "block"
                        : "none";
            }

        }

        if(checkboxDose){

            checkboxDose.addEventListener(
                "change",
                atualizarCampos
            );

        }

        if(checkboxUnidade){

            checkboxUnidade.addEventListener(
                "change",
                atualizarCampos
            );

        }

        atualizarCampos();

    }
);

const checkboxUnidade =
    document.getElementById(
        "vende_por_unidade"
    );

const campoUnidade =
    document.getElementById(
        "campo-unidade"
    );

if(
    checkboxUnidade &&
    campoUnidade
){

    checkboxUnidade.addEventListener(
        "change",
        () => {

            campoUnidade.style.display =
                checkboxUnidade.checked
                    ? "block"
                    : "none";

        }
    );

}