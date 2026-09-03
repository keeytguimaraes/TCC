document.addEventListener(
    "DOMContentLoaded",
    function(){

        // ==========================
        // CAMPOS DE MOTIVO
        // ==========================

        const tipoMovimentacao =
            document.querySelector(
                '[name="tipo_movimentacao"]'
            );

        const campoMotivo =
            document.getElementById(
                "motivo"
            );

        const grupoMotivo =
            document.getElementById(
                "grupo-motivo"
            );

        function atualizarMotivo(){

            if(
                tipoMovimentacao.value === "uso_interno" ||
                tipoMovimentacao.value === "ajuste_manual"
            ){

                grupoMotivo.style.display =
                    "block";

                campoMotivo.required =
                    true;

            }
            else{

                grupoMotivo.style.display =
                    "none";

                campoMotivo.required =
                    false;

                campoMotivo.value =
                    "";

            }

        }

        tipoMovimentacao.addEventListener(
            "change",
            atualizarMotivo
        );

        atualizarMotivo();

        // ==========================
        // PRODUTO
        // ==========================

        const produtoMovimentacao =
            document.getElementById(
                "produto_movimentacao"
            );

        if(
            !produtoMovimentacao
        ){
            return;
        }

        // ==========================
        // GRUPOS
        // ==========================

        const grupoCaixa =
            document.getElementById(
                "grupo-caixa"
            );

        const grupoUnidade =
            document.getElementById(
                "grupo-unidade"
            );

        const grupoFracionado =
            document.getElementById(
                "grupo-fracionado"
            );

        // ==========================
        // LABELS
        // ==========================

        const labelCaixa =
            document.getElementById(
                "label-caixa"
            );

        const labelUnidade =
            document.getElementById(
                "label-unidade"
            );

        const labelFracionado =
            document.getElementById(
                "label-fracionado"
            );

        // ==========================
        // ATUALIZA CAMPOS
        // ==========================

        function atualizarCampos(){

            const opcaoSelecionada =
                produtoMovimentacao.options[
                    produtoMovimentacao.selectedIndex
                ];

            const quantidadePorCaixa =
                Number(
                    opcaoSelecionada.dataset.caixa
                ) || 0;

            const vendePorUnidade =
                Number(
                    opcaoSelecionada.dataset.unidade
                ) || 0;

            const vendePorDose =
                Number(
                    opcaoSelecionada.dataset.dose
                ) || 0;

            const categoria =
                (
                    opcaoSelecionada.dataset.categoria || ""
                ).toLowerCase();

            // ==========================
            // NOMES DOS CAMPOS
            // ==========================

            if(
                categoria.includes(
                    "cigarro"
                )
            ){

                labelCaixa.textContent =
                    "Box";

                labelUnidade.textContent =
                    "Maços";

                labelFracionado.textContent =
                    "Cigarros Avulsos";

            }

            else if(
                vendePorDose === 1
            ){

                labelCaixa.textContent =
                    "Caixas";

                labelUnidade.textContent =
                    "Unidades";

                labelFracionado.textContent =
                    "Doses";

            }

            else{

                labelCaixa.textContent =
                    "Caixas";

                labelUnidade.textContent =
                    "Unidades";

                labelFracionado.textContent =
                    "Quantidade Avulsa";

            }

            // ==========================
            // CAIXA
            // ==========================

            if(
                quantidadePorCaixa > 1
            ){

                grupoCaixa.style.display =
                    "block";

            }
            else{

                grupoCaixa.style.display =
                    "none";

            }

            // ==========================
            // UNIDADE / MAÇO
            // ==========================

            if(
                vendePorUnidade === 1
            ){

                grupoUnidade.style.display =
                    "block";

            }
            else{

                grupoUnidade.style.display =
                    "none";

            }

            // ==========================
            // DOSE / AVULSO
            // ==========================

            if(
                vendePorDose === 1 ||
                categoria.includes(
                    "cigarro"
                )
            ){

                grupoFracionado.style.display =
                    "block";

            }
            else{

                grupoFracionado.style.display =
                    "none";

            }

        }

        produtoMovimentacao.addEventListener(
            "change",
            atualizarCampos
        );

        atualizarCampos();

    }
);