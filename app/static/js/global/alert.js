document.addEventListener(
    "DOMContentLoaded",
    function(){

        const alertas =
            document.querySelectorAll(
                ".alert"
            );

        alertas.forEach(

            function(alerta){

                setTimeout(

                    function(){

                        alerta.style.opacity = "0";

                        setTimeout(

                            function(){

                                alerta.remove();

                            },

                            500

                        );

                    },

                    5000

                );

            }

        );

    }

);
