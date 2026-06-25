from flask import (
    render_template
)

from app.controllers.relatorio_controller import (
    pegar_relatorio
)


def configurar_relatorio_routes(app):

    @app.route("/relatorio")
    def relatorio():

        dados = pegar_relatorio()

        return render_template(

            "relatorio/relatorio.html",

            dados=dados
        )