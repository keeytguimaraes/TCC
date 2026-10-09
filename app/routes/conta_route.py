
# ============================================================
# ROTAS DE CONTAS — SIGC
# ============================================================
# Este arquivo reúne as rotas relacionadas ao gerenciamento
# de contas pendentes.
#
# Funcionalidades:
# - Listar contas pendentes;
# - Consultar os clientes disponíveis;
# - Receber o pagamento de uma conta;
# - Marcar as vendas relacionadas como pagas;
# - Exibir a tela de transferência de conta;
# - Transferir uma conta pendente para o fiado de um cliente.
#
# As rotas recebem as requisições do navegador e chamam
# os controllers ou models responsáveis pelas operações.
# ============================================================


# Importa o decorator que exige autenticação do usuário.
from app.utils.auth import login_obrigatorio

# Importa as ferramentas necessárias do Flask:
# - render_template: exibe uma página HTML;
# - redirect: redireciona para outra rota;
# - flash: prepara uma mensagem temporária para a interface;
# - request: permite ler os dados enviados pelos formulários.
from flask import (
    render_template,
    redirect,
    flash,
    request
)

# Importa a função responsável por buscar as contas.
from app.controllers.conta_controller import (
    pegar_contas
)

# Importa a função que lista os clientes cadastrados.
from app.models.cliente_model import (
    listar_clientes
)

# Importa a função que abre uma conexão com o PostgreSQL.
from app.database.conexao import conectar

# Importa a função responsável por transferir uma conta
# pendente para o fiado de um cliente.
from app.models.conta_model import (
    transferir_para_fiado
)


# ============================================================
# CONFIGURAR ROTAS DE CONTAS
# ============================================================
def configurar_conta_routes(app):
    """
    Registra as rotas de contas na aplicação Flask.

    Parâmetros:
        app: instância principal da aplicação Flask.

    As rotas são registradas na aplicação por meio dos
    decorators @app.route.
    """

    # --------------------------------------------------------
    # LISTAR CONTAS
    # --------------------------------------------------------
    # URL: /conta
    # Método: GET
    #
    # Exibe as contas e a lista de clientes disponibilizada
    # ao template.
    @app.route("/conta")
    @login_obrigatorio
    def conta():
        """
        Busca as contas e os clientes para exibir a página.

        A proteção login_obrigatorio exige que o usuário esteja
        autenticado para acessar esta rota.
        """

        # Busca as contas por meio do controller.
        contas = pegar_contas()

        # Busca os clientes para disponibilizá-los na interface.
        clientes = listar_clientes()

        # Renderiza a página de contas, enviando os dados
        # necessários para o template.
        return render_template(
            "conta/conta.html",
            contas=contas,
            clientes=clientes
        )

    # --------------------------------------------------------
    # RECEBER PAGAMENTO DE UMA CONTA
    # --------------------------------------------------------
    # URL: /conta/pagar/<conta_id>
    # Método: POST
    #
    # Atualiza o status da conta pendente para "Quitada"
    # e altera o status de pagamento das vendas relacionadas
    # para "pago".
    @app.route(
        "/conta/pagar/<int:conta_id>",
        methods=["POST"]
    )
    def pagar_conta(conta_id):
        """
        Registra a quitação de uma conta pendente.

        Parâmetros:
            conta_id: ID da conta que será quitada.

        As duas atualizações são executadas na mesma conexão
        e confirmadas por meio de um único commit.
        """

        # Abre a conexão com o banco de dados.
        conexao = conectar()

        # Cria o cursor responsável pela execução dos comandos SQL.
        cursor = conexao.cursor()

        # ----------------------------------------------------
        # 1. MARCAR A CONTA COMO QUITADA
        # ----------------------------------------------------
        # Atualiza o status da conta cujo ID foi informado.
        sql_conta = """
            UPDATE conta_pendente
            SET status = 'Quitada'
            WHERE id = %s
        """

        cursor.execute(
            sql_conta,
            (conta_id,)
        )

        # ----------------------------------------------------
        # 2. MARCAR AS VENDAS COMO PAGAS
        # ----------------------------------------------------
        # Atualiza o status das vendas vinculadas à conta
        # pendente informada.
        sql_vendas = """
            UPDATE venda
            SET status_pagamento = 'pago'
            WHERE conta_pendente_id = %s
        """

        cursor.execute(
            sql_vendas,
            (conta_id,)
        )

        # ----------------------------------------------------
        # 3. CONFIRMAR AS ALTERAÇÕES
        # ----------------------------------------------------
        # Confirma as duas atualizações no banco de dados.
        conexao.commit()

        # Fecha o cursor e a conexão após a operação.
        cursor.close()
        conexao.close()

        # Prepara uma mensagem de confirmação para a interface.
        flash(
            "Conta quitada com sucesso!",
            "success"
        )

        # Retorna à listagem de contas.
        return redirect("/conta")

    # --------------------------------------------------------
    # ABRIR TELA DE TRANSFERÊNCIA
    # --------------------------------------------------------
    # URL: /conta/transferir/<conta_id>
    # Método: GET
    #
    # Exibe a tela na qual o usuário pode selecionar um cliente
    # para transferir a conta pendente para o fiado.
    @app.route(
        "/conta/transferir/<int:conta_id>"
    )
    def tela_transferir_conta(conta_id):
        """
        Carrega os clientes e apresenta a tela de transferência.

        Parâmetros:
            conta_id: ID da conta pendente que será transferida.
        """

        # Busca os clientes disponíveis para seleção.
        clientes = listar_clientes()

        # Renderiza o formulário de transferência.
        #
        # O ID da conta é enviado ao template para que o
        # formulário possa identificar a conta selecionada.
        return render_template(
            "conta/transferir_conta.html",
            conta_id=conta_id,
            clientes=clientes
        )

    # --------------------------------------------------------
    # CONFIRMAR TRANSFERÊNCIA PARA O FIADO
    # --------------------------------------------------------
    # URL: /conta/transferir/confirmar/<conta_id>
    # Método: POST
    #
    # Recebe o cliente selecionado e solicita ao model que
    # realize a transferência da conta para o fiado.
    @app.route(
        "/conta/transferir/confirmar/<int:conta_id>",
        methods=["POST"]
    )
    def confirmar_transferencia(conta_id):
        """
        Transfere uma conta pendente para o fiado de um cliente.

        Parâmetros:
            conta_id: ID da conta pendente que será transferida.

        O cliente selecionado é obtido pelo campo cliente_id
        enviado pelo formulário.
        """

        # Obtém o ID do cliente selecionado na tela.
        cliente_id = request.form.get(
            "cliente_id"
        )

        # Chama o model para realizar a transferência.
        # A regra de negócio permanece na função importada.
        transferir_para_fiado(
            conta_id,
            cliente_id
        )

        # Informa que a operação foi concluída.
        flash(
            "Conta transferida com sucesso!",
            "success"
        )

        # Redireciona para a tela de fiado.
        return redirect("/fiado")
