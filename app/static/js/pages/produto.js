/* ==========================================================
   PRODUTOS — campos condicionais (venda por dose / avulsa)
   Usado pelo modal de cadastro (produto.html) e pela edição
   (editar_produto.html).

   Mantém os ids originais e a mesma regra: marcar a opção
   mostra os campos; desmarcar esconde. Os valores digitados
   são preservados ao alternar. Os campos escondidos usam o
   atributo [hidden] (e não style.display), para não quebrar
   o layout em grade.
   ========================================================== */

   document.addEventListener("DOMContentLoaded", () => {

    const grupos = [
        {
            checkbox: "vende_por_dose",
            // blocos que aparecem quando a opção está marcada
            campos: [
                "grupo-dose",
                "campo-dose",
                "campo-preco-dose"
            ],
            // campos exigidos somente enquanto a opção está marcada
            obrigatorios: [
                "volume_dose_ml",
                "preco_dose"
            ]
        },
        {
            checkbox: "vende_por_unidade",
            campos: [
                "grupo-unidade",
                "campo-unidade",
                "campo-preco-unidade",
                "campo-quantidade-unidade"
            ],
            obrigatorios: [
                "preco_unidade"
            ]
        }
    ];

    grupos.forEach((grupo) => {

        const checkbox = document.getElementById(grupo.checkbox);

        if (!checkbox) return;

        const formulario = checkbox.form;

        function atualizar() {

            const mostrar = checkbox.checked;

            grupo.campos.forEach((id) => {

                const elemento = document.getElementById(id);

                if (elemento) {
                    elemento.hidden = !mostrar;
                }

            });

            // Campo escondido não pode bloquear o envio do formulário.
            grupo.obrigatorios.forEach((nome) => {

                const campo = formulario && formulario.elements[nome];

                if (campo) {
                    campo.required = mostrar;
                }

            });

        }

        checkbox.addEventListener("change", atualizar);

        atualizar();

    });

});