# Importa Flask
from flask import (
    render_template,
    redirect
)

# Importa controller
from app.controllers.conta_controller import (
    pegar_contas
)


# ==========================
# CONFIGURAR ROTAS
# ==========================
def configurar_conta_routes(app):

    # ==========================
    # LISTAR CONTAS
    # ==========================
    @app.route("/conta")
    def conta():

        contas = pegar_contas()

        return render_template(

            "conta/conta.html",

            contas=contas
        )
    # ==========================
    # RECEBER PAGAMENTO
    # ==========================
    @app.route(
        "/conta/pagar/<int:venda_id>",
        methods=["POST"]
    )
    def pagar_conta(

        venda_id
    ):

        from app.database.conexao import (
            conectar
        )

        conexao = conectar()

        cursor = conexao.cursor()

        sql = """
        UPDATE venda

        SET status_pagamento = 'Pago'

        WHERE id = %s
    """

        cursor.execute(

            sql,

            (
                venda_id,
            )
        )

        conexao.commit()

        cursor.close()

        conexao.close()

        return redirect(
            "/conta"
        )