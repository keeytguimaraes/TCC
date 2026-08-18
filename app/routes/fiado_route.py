from flask import (
    render_template,
    request,
    redirect
)

from app.controllers.fiado_controller import (
    pegar_fiados,
    pegar_fiado_detalhes,
    receber_pagamento_fiado
)


def configurar_fiado_routes(app):

    # ==========================
    # LISTAR FIADOS
    # ==========================
    @app.route("/fiado")
    def fiado():

        fiados = pegar_fiados()

        return render_template(

            "fiado/fiado.html",

            fiados=fiados
        )


    # ==========================
    # DETALHES DO FIADO
    # ==========================
    @app.route(
        "/fiado/detalhes/<int:conta_id>"
    )
    def detalhes_fiado(conta_id):

        fiado = pegar_fiado_detalhes(
            conta_id
        )

        return render_template(

            "fiado/detalhes_fiado.html",

            fiado=fiado
        )


    # ==========================
    # RECEBER PAGAMENTO FIADO
    # ==========================
    @app.route(
        "/fiado/receber/<int:conta_id>",
        methods=["POST"]
    )
    def receber_pagamento(conta_id):

        valor_recebido = request.form.get(
            "valor_recebido"
        )

        receber_pagamento_fiado(

            conta_id,

            valor_recebido
        )

        return redirect(
    f"/fiado/detalhes/{conta_id}"
)