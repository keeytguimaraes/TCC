document.addEventListener("DOMContentLoaded", () => {

    const checkbox =
        document.getElementById(
            "vende_por_dose"
        );

    const campoDose =
        document.getElementById(
            "campo-dose"
        );

    if(
        !checkbox ||
        !campoDose
    ){
        return;
    }

    checkbox.addEventListener(
        "change",
        () => {

            if(
                checkbox.checked
            ){

                campoDose.style.display =
                    "block";

            }else{

                campoDose.style.display =
                    "none";

            }

        }
    );

});