from flask import (
    render_template,
    request,
    redirect
)

from app.controllers.fiado_controller import (
    pegar_fiados,
    receber_pagamento_fiado
)


def configurar_fiado_routes(app):

    @app.route("/fiado")
    def fiado():

        fiados = pegar_fiados()

        return render_template(

            "fiado/fiado.html",

            fiados=fiados
        )
    
    # ==========================
    # RECEBER PAGAMENTO FIADO
    # ==========================
    @app.route(
        "/fiado/receber/<int:venda_id>",
        methods=["POST"]
    )
    def receber_pagamento(

        venda_id
    ):

        valor_recebido = request.form.get(

            "valor_recebido"
        )

        receber_pagamento_fiado(

            venda_id,

            valor_recebido
        )

        return redirect(
            "/fiado"
        )