
# ============================================================
# ROTAS DE FIADO — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis pelo gerenciamento
# das contas de fiado dos clientes.
#
# Funcionalidades:
# - Listar as contas de fiado;
# - Consultar os detalhes de uma conta;
# - Registrar o recebimento de um pagamento;
# - Localizar a conta de fiado de um cliente.
#
# As rotas recebem as requisições do navegador e encaminham
# as operações ao fiado_controller.
# ============================================================


# Importa o decorator que exige autenticação do usuário.
from app.utils.auth import (
    login_obrigatorio
)

# Importa as ferramentas necessárias do Flask:
# - render_template: apresenta uma página HTML;
# - request: acessa os dados enviados pelo formulário;
# - redirect: redireciona para outra URL;
# - flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller de fiado.
from app.controllers.fiado_controller import (
    pegar_fiados,
    pegar_fiado_detalhes,
    receber_pagamento_fiado,
    pegar_conta_cliente
)


# ============================================================
# CONFIGURAR ROTAS DE FIADO
# ============================================================
def configurar_fiado_routes(app):
    """
    Registra as rotas de gerenciamento de fiado na aplicação.

    Parâmetros:
        app: instância principal da aplicação Flask.

    As rotas são registradas na aplicação pelos decorators
    @app.route definidos dentro desta função.
    """

    # --------------------------------------------------------
    # LISTAR CONTAS DE FIADO
    # --------------------------------------------------------
    # URL: /fiado
    # Método: GET
    #
    # Busca as contas de fiado e exibe a página de listagem.
    # Esta rota exige que o usuário esteja autenticado.
    @app.route("/fiado")
    @login_obrigatorio
    def fiado():
        """
        Busca as contas de fiado e apresenta a listagem.
        """

        # Solicita ao controller os registros de fiado.
        fiados = pegar_fiados()

        # Renderiza a página e disponibiliza os registros
        # na variável fiados, que poderá ser utilizada
        # pelo template fiado.html.
        return render_template(
            "fiado/fiado.html",
            fiados=fiados
        )

    # --------------------------------------------------------
    # CONSULTAR DETALHES DO FIADO
    # --------------------------------------------------------
    # URL: /fiado/detalhes/<conta_id>
    # Método: GET
    #
    # Busca os detalhes da conta identificada pelo ID
    # recebido na URL.
    @app.route(
        "/fiado/detalhes/<int:conta_id>"
    )
    def detalhes_fiado(conta_id):
        """
        Busca e apresenta os detalhes de uma conta de fiado.

        Parâmetros:
            conta_id: identificador da conta de fiado.
        """

        # Solicita ao controller os dados da conta selecionada.
        fiado = pegar_fiado_detalhes(
            conta_id
        )

        # Renderiza a página de detalhes e envia os dados
        # retornados pelo controller.
        return render_template(
            "fiado/detalhes_fiado.html",
            fiado=fiado
        )

    # --------------------------------------------------------
    # RECEBER PAGAMENTO DE FIADO
    # --------------------------------------------------------
    # URL: /fiado/receber/<conta_id>
    # Método: POST
    #
    # Recebe o valor informado no formulário e encaminha
    # a operação ao controller responsável pelo pagamento.
    @app.route(
        "/fiado/receber/<int:conta_id>",
        methods=["POST"]
    )
    def receber_pagamento(conta_id):
        """
        Registra um recebimento relacionado à conta de fiado.

        Parâmetros:
            conta_id: identificador da conta que receberá
            o pagamento.

        O valor recebido é obtido do formulário e encaminhado
        ao controller, que realiza o processamento.
        """

        # Obtém o valor enviado pelo campo valor_recebido.
        valor_recebido = request.form.get(
            "valor_recebido"
        )

        # Encaminha o ID da conta e o valor recebido
        # ao controller de fiado.
        receber_pagamento_fiado(
            conta_id,
            valor_recebido
        )

        # Prepara uma mensagem de confirmação para ser exibida
        # na página seguinte.
        flash(
            "Pagamento recebido com sucesso!",
            "success"
        )

        # Retorna à página de detalhes da mesma conta,
        # utilizando seu ID para montar a URL.
        return redirect(
            f"/fiado/detalhes/{conta_id}"
        )

    # --------------------------------------------------------
    # ABRIR FIADO PELO CLIENTE
    # --------------------------------------------------------
    # URL: /cliente/fiado/<cliente_id>
    # Método: GET
    #
    # Busca a conta de fiado associada ao cliente.
    # Se encontrar uma conta, redireciona para os detalhes.
    # Caso contrário, retorna à listagem geral de fiados.
    @app.route(
        "/cliente/fiado/<int:cliente_id>"
    )
    def abrir_fiado_cliente(cliente_id):
        """
        Localiza a conta de fiado de um cliente.

        Parâmetros:
            cliente_id: identificador do cliente.

        O controller retorna a conta encontrada ou um resultado
        falso quando não existe uma conta correspondente.
        """

        # Busca a conta de fiado associada ao cliente informado.
        conta = pegar_conta_cliente(
            cliente_id
        )

        # Se nenhuma conta for encontrada, retorna à listagem.
        if not conta:
            return redirect("/fiado")

        # Se a conta existir, abre sua página de detalhes.
        # O ID da conta é obtido do resultado retornado
        # pelo controller.
        return redirect(
            f"/fiado/detalhes/{conta['id']}"
        )
