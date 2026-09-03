from flask import (

    render_template,
    request,
    redirect,
    flash

)

from app.controllers.movimentacao_controller import (

    pegar_produtos_movimentacao,

    cadastrar_movimentacao_controller
)

from app.controllers.movimentacao_controller import (

    pegar_produtos_movimentacao,

    cadastrar_movimentacao_controller,

    pegar_movimentacoes
)


def configurar_movimentacao_routes(app):

    # ==========================
    # TELA
    # ==========================
    @app.route("/movimentacao")

    def movimentacao():

        produtos = pegar_produtos_movimentacao()

        return render_template(

            "estoque/movimentacao.html",

            produtos=produtos
        )


    # ==========================
    # CADASTRAR MOVIMENTAÇÃO
    # ==========================
    @app.route(
    "/movimentacao/cadastrar",
    methods=["POST"]
)
    def cadastrar_movimentacao_route():

        try:

            produto_id = request.form.get(
            "produto_id"
        )

            tipo_movimentacao = request.form.get(
            "tipo_movimentacao"
        )

            quantidade_caixa = int(
            request.form.get(
                "quantidade_caixa",
                0
            ) or 0
        )

            quantidade_unidade = int(
            request.form.get(
                "quantidade_unidade",
                0
            ) or 0
        )

            quantidade_fracionada = int(
            request.form.get(
                "quantidade_fracionada",
                0
            ) or 0
        )

            motivo = request.form.get(
            "motivo"
        )

            cadastrar_movimentacao_controller(

            produto_id,
            tipo_movimentacao,
            quantidade_caixa,
            quantidade_unidade,
            quantidade_fracionada,
            motivo

        )

            flash(
            "Movimentação registrada com sucesso!",
            "success"
        )

        except Exception as erro:

            flash(
            str(erro),
            "error"
        )

        return redirect("/estoque")

    # ==========================
    # HISTÓRICO MOVIMENTAÇÃO
    # ==========================
    @app.route(
    "/movimentacao/historico"
)
    def historico_movimentacao():

        movimentacoes = pegar_movimentacoes()

        return render_template(

        "estoque/historico_movimentacao.html",

        movimentacoes=movimentacoes
    )