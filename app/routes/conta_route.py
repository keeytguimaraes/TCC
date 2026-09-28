# Importa Flask
from flask import (
    render_template,
    redirect,
    flash
)

# Importa controller
from app.controllers.conta_controller import (
    pegar_contas
)

from app.models.cliente_model import listar_clientes


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

        clientes = listar_clientes()

        return render_template(

        "conta/conta.html",

        contas=contas,

        clientes=clientes
    )
    # ==========================
    # RECEBER PAGAMENTO
    # ==========================
    @app.route(
    "/conta/pagar/<int:conta_id>",
    methods=["POST"]
)
    def pagar_conta(conta_id):

        from app.database.conexao import (
        conectar
    )

        conexao = conectar()

        cursor = conexao.cursor()

        # ----------------------
        # FECHA CONTA
        # ----------------------
        sql_conta = """
        UPDATE conta_pendente

        SET status = 'Quitada'

        WHERE id = %s
    """

        cursor.execute(
        sql_conta,
        (conta_id,)
    )

        # ----------------------
        # MARCA VENDAS COMO PAGAS
        # ----------------------
        sql_vendas = """
        UPDATE venda

        SET status_pagamento = 'Pago'

        WHERE conta_pendente_id = %s
    """

        cursor.execute(
        sql_vendas,
        (conta_id,)
    )

        conexao.commit()

        cursor.close()
        conexao.close()

        flash(
    "Conta quitada com sucesso!",
    "success"
)

        return redirect(
        "/conta"
    )

    # ==========================
    # TELA TRANSFERIR
    # ==========================
    @app.route(
    "/conta/transferir/<int:conta_id>"
)
    def tela_transferir_conta(conta_id):

        from app.models.cliente_model import (
        listar_clientes
    )

        clientes = listar_clientes()

        return render_template(

        "conta/transferir_conta.html",

        conta_id=conta_id,

        clientes=clientes
    )

    # ==========================
    # CONFIRMAR TRANSFERÊNCIA
    # ==========================
    @app.route(
    "/conta/transferir/confirmar/<int:conta_id>",
    methods=["POST"]
)
    def confirmar_transferencia(conta_id):

        from flask import request

        from app.models.conta_model import (
        transferir_para_fiado
    )

        cliente_id = request.form.get(
        "cliente_id"
    )

        transferir_para_fiado(

        conta_id,

        cliente_id
    )
        
        flash(
    "Conta transferida com sucesso!",
    "success"
)

        return redirect(
        "/fiado"
    )