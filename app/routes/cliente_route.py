
# ============================================================
# ROTAS DE CLIENTES — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis pelo gerenciamento
# dos clientes cadastrados no Sistema Integrado de Gestão
# Comercial (SIGC).
#
# Funcionalidades:
# - Listar clientes ativos;
# - Cadastrar clientes;
# - Abrir a tela de edição;
# - Salvar alterações nos dados do cliente;
# - Desativar clientes;
# - Listar clientes inativos;
# - Reativar clientes.
#
# As rotas recebem as requisições HTTP e chamam os controllers,
# que são responsáveis por executar as operações relacionadas
# aos dados dos clientes.
# ============================================================


# Importa os decorators utilizados para controlar o acesso.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas do Flask:
# - render_template: exibe uma página HTML;
# - request: acessa os dados enviados pelo formulário;
# - redirect: redireciona para outra rota;
# - flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller de clientes.
#
# O controller faz a ligação entre as rotas e o modelo,
# concentrando as operações relacionadas aos clientes.
from app.controllers.cliente_controller import (
    pegar_clientes,
    cadastrar_cliente_controller,
    desativar_cliente_controller,
    buscar_cliente_controller,
    editar_cliente_controller,
    listar_clientes_inativos_controller,
    reativar_cliente_controller
)


# ============================================================
# CONFIGURAR ROTAS DE CLIENTES
# ============================================================
def configurar_cliente_routes(app):
    """
    Registra as rotas de gerenciamento de clientes na aplicação.

    Parâmetros:
        app: instância principal da aplicação Flask.

    As funções de rota são definidas dentro desta função
    e registradas por meio dos decorators @app.route.
    """

    # --------------------------------------------------------
    # LISTAR CLIENTES
    # --------------------------------------------------------
    # URL: /cliente
    #
    # Exibe a lista de clientes ativos.
    #
    # Proteção existente:
    # - O usuário precisa estar autenticado;
    # - O perfil precisa ser administrador ou gerente.
    @app.route("/cliente")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def cliente():
        """
        Busca os clientes e apresenta a página de listagem.

        Os dados obtidos pelo controller são enviados ao
        template por meio da variável clientes.
        """

        # Busca os clientes disponíveis para a listagem.
        dados = pegar_clientes()

        # Renderiza a página e disponibiliza os registros
        # para que o template possa apresentá-los.
        return render_template(
            "cliente/cliente.html",
            clientes=dados
        )

    # --------------------------------------------------------
    # CADASTRAR CLIENTE
    # --------------------------------------------------------
    # URL: /cliente/cadastrar
    # Método: POST
    #
    # Recebe o nome informado no formulário e solicita
    # ao controller o cadastro do cliente.
    @app.route(
        "/cliente/cadastrar",
        methods=["POST"]
    )
    def cadastrar_cliente():
        """
        Recebe os dados do formulário e cadastra um cliente.
        """

        # Obtém o conteúdo do campo "nome" enviado pelo
        # formulário HTML.
        nome = request.form.get("nome")

        # Encaminha o nome ao controller para realizar
        # o cadastro conforme as regras existentes.
        cadastrar_cliente_controller(nome)

        # Prepara uma mensagem de sucesso para ser exibida
        # na próxima página carregada.
        flash(
            "Cliente cadastrado com sucesso!",
            "success"
        )

        # Retorna à listagem de clientes.
        return redirect("/cliente")

    # --------------------------------------------------------
    # ABRIR TELA DE EDIÇÃO
    # --------------------------------------------------------
    # URL: /cliente/editar/<id_cliente>
    # Método: GET
    #
    # Busca os dados do cliente para preencher o formulário
    # de edição com as informações atuais.
    @app.route(
        "/cliente/editar/<int:id_cliente>"
    )
    def tela_editar_cliente(id_cliente):
        """
        Busca um cliente pelo ID e abre sua tela de edição.

        Parâmetros:
            id_cliente: identificador do cliente na URL.
        """

        # Solicita ao controller os dados do cliente.
        cliente = buscar_cliente_controller(
            id_cliente
        )

        # Renderiza o formulário de edição e disponibiliza
        # os dados encontrados na variável cliente.
        return render_template(
            "cliente/editar_cliente.html",
            cliente=cliente
        )

    # --------------------------------------------------------
    # SALVAR EDIÇÃO DO CLIENTE
    # --------------------------------------------------------
    # URL: /cliente/editar/<id_cliente>
    # Método: POST
    #
    # A mesma URL utilizada para abrir o formulário recebe
    # os dados enviados quando o usuário salva a edição.
    @app.route(
        "/cliente/editar/<int:id_cliente>",
        methods=["POST"]
    )
    def editar_cliente(id_cliente):
        """
        Atualiza o nome de um cliente existente.

        Parâmetros:
            id_cliente: identificador do cliente que será editado.
        """

        # Obtém o novo nome enviado pelo formulário.
        nome = request.form.get("nome")

        # Solicita ao controller a atualização do registro.
        # O ID identifica qual cliente deve ser alterado.
        editar_cliente_controller(
            id_cliente,
            nome
        )

        # Prepara a mensagem de confirmação da alteração.
        flash(
            "Cliente atualizado com sucesso!",
            "success"
        )

        # Retorna à listagem principal.
        return redirect("/cliente")

    # --------------------------------------------------------
    # DESATIVAR CLIENTE
    # --------------------------------------------------------
    # URL: /cliente/desativar/<cliente_id>
    # Método: POST
    #
    # Solicita a desativação do cliente sem excluir
    # permanentemente seu registro do banco de dados.
    @app.route(
        "/cliente/desativar/<int:cliente_id>",
        methods=["POST"]
    )
    def desativar_cliente(cliente_id):
        """
        Desativa o cliente identificado pelo ID recebido.
        """

        # Encaminha o identificador ao controller.
        desativar_cliente_controller(
            cliente_id
        )

        # Retorna à listagem de clientes.
        return redirect("/cliente")

    # --------------------------------------------------------
    # LISTAR CLIENTES INATIVOS
    # --------------------------------------------------------
    # URL: /cliente/inativos
    #
    # Busca os clientes inativos e exibe a página específica
    # que permite consultar esses registros.
    @app.route("/cliente/inativos")
    def clientes_inativos():
        """
        Apresenta a listagem de clientes desativados.
        """

        # Busca os clientes inativos por meio do controller.
        dados = listar_clientes_inativos_controller()

        # Renderiza a página e disponibiliza os registros.
        return render_template(
            "cliente/clientes_inativos.html",
            clientes=dados
        )

    # --------------------------------------------------------
    # REATIVAR CLIENTE
    # --------------------------------------------------------
    # URL: /cliente/reativar/<cliente_id>
    # Método: POST
    #
    # Solicita ao controller que reative o cliente selecionado.
    @app.route(
        "/cliente/reativar/<int:cliente_id>",
        methods=["POST"]
    )
    def reativar_cliente(cliente_id):
        """
        Reativa um cliente que estava desativado.
        """

        # Encaminha o ID do cliente ao controller.
        reativar_cliente_controller(
            cliente_id
        )

        # Após a operação, retorna à lista de inativos.
        return redirect(
            "/cliente/inativos"
        )
