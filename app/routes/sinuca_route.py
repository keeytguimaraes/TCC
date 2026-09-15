from flask import (

    render_template,

    request,

    redirect
)

from app.controllers.sinuca_controller import (

    pegar_config_sinuca,

    salvar_config_sinuca,

    pegar_dados_relatorio_sinuca
)


def configurar_sinuca_routes(app):

        # ==========================
    # TELA DA SINUCA
    # ==========================
    @app.route("/sinuca")
    def sinuca():

        config = pegar_config_sinuca()

        dados = pegar_dados_relatorio_sinuca()

        return render_template(

        "sinuca/configuracao_sinuca.html",

        config=config,

        dados=dados
    )
    
    # ==========================
    # SALVAR CONFIGURAÇÃO
    # ==========================
    @app.route(

        "/sinuca/salvar",

        methods=["POST"]
    )
    def salvar_sinuca():

        nome = request.form.get(
            "nome"
        )

        valor_ficha = request.form.get(
            "valor_ficha"
        )

        percentual_comercio = request.form.get(
            "percentual_comercio"
        )

        salvar_config_sinuca(

            nome,

            valor_ficha,

            percentual_comercio,

        )

        return redirect(
            "/sinuca"
        )