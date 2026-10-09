
# ============================================================
# ROTAS DE FORNECEDORES — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis pelo gerenciamento
# dos fornecedores cadastrados no sistema.
#
# Funcionalidades:
# - Listar fornecedores;
# - Cadastrar fornecedores;
# - Abrir a tela de edição;
# - Salvar alterações nos dados do fornecedor;
# - Listar fornecedores inativos;
# - Reativar fornecedores;
# - Desativar fornecedores.
#
# As rotas recebem as requisições do navegador e encaminham
# as operações aos controllers ou às funções de modelo
# responsáveis pelo gerenciamento dos fornecedores.
# ============================================================


# Importa os decorators de autenticação e autorização.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas do Flask:
# - render_template: apresenta páginas HTML;
# - request: acessa os dados enviados pelo formulário;
# - redirect: redireciona o usuário para outra URL;
# - flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller de fornecedores.
from app.controllers.fornecedor_controller import (
    pegar_fornecedores,
    cadastrar_fornecedor_controller,
    pegar_fornecedor_por_id,
    editar_fornecedor_controller,
    pegar_fornecedores_inativos,
    reativar_fornecedor,
    desativar_fornecedor_controller
)


# ============================================================
# CONFIGURAR ROTAS DE FORNECEDORES
# ============================================================
def configurar_fornecedor_routes(app):
    """
    Registra as rotas de gerenciamento de fornecedores.

    Parâmetros:
        app: instância principal da aplicação Flask.

    As rotas são registradas na aplicação por meio dos
    decorators @app.route.
    """

    # --------------------------------------------------------
    # LISTAR FORNECEDORES
    # --------------------------------------------------------
    # URL: /fornecedor
    # Método: GET
    #
    # Esta rota exige autenticação e um dos seguintes perfis:
    # administrador ou gerente.
    @app.route("/fornecedor")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def fornecedor():
        """
        Busca os fornecedores e apresenta a página de listagem.
        """

        # Solicita ao controller a lista de fornecedores.
        dados = pegar_fornecedores()

        # Renderiza a página e envia os dados encontrados
        # para o template por meio da variável fornecedores.
        return render_template(
            "fornecedor/fornecedor.html",
            fornecedores=dados
        )

    # --------------------------------------------------------
    # CADASTRAR FORNECEDOR
    # --------------------------------------------------------
    # URL: /fornecedor/cadastrar
    # Método: POST
    #
    # Recebe os dados do formulário e encaminha as informações
    # ao controller responsável pelo cadastro.
    @app.route(
        "/fornecedor/cadastrar",
        methods=["POST"]
    )
    def cadastrar_fornecedor_route():
        """
        Cadastra um fornecedor a partir dos dados do formulário.
        """

        # Obtém o nome informado no formulário.
        nome = request.form.get("nome")

        # Obtém o telefone informado.
        telefone = request.form.get("telefone")

        # Obtém a observação, quando preenchida.
        observacao = request.form.get("observacao")

        # Encaminha os três valores ao controller.
        cadastrar_fornecedor_controller(
            nome,
            telefone,
            observacao
        )

        # Prepara a mensagem de sucesso para a próxima página.
        flash(
            "Fornecedor cadastrado com sucesso!",
            "success"
        )

        # Retorna à listagem de fornecedores.
        return redirect("/fornecedor")

    # --------------------------------------------------------
    # EDITAR FORNECEDOR
    # --------------------------------------------------------
    # URL: /fornecedor/editar/<id_fornecedor>
    # Métodos: GET e POST
    #
    # GET:
    # Busca os dados atuais e exibe o formulário.
    #
    # POST:
    # Recebe os dados alterados, chama o controller
    # e redireciona para a listagem.
    @app.route(
        "/fornecedor/editar/<int:id_fornecedor>",
        methods=["GET", "POST"]
    )
    def editar_fornecedor_route(id_fornecedor):
        """
        Exibe o formulário de edição ou salva as alterações.

        Parâmetros:
            id_fornecedor: identificador do fornecedor na URL.
        """

        # ----------------------------------------------------
        # REQUISIÇÃO POST: SALVAR ALTERAÇÕES
        # ----------------------------------------------------
        if request.method == "POST":

            # Lê o novo nome enviado pelo formulário.
            nome = request.form.get("nome")

            # Lê o novo telefone.
            telefone = request.form.get("telefone")

            # Lê a nova observação.
            observacao = request.form.get("observacao")

            # Solicita ao controller a atualização do fornecedor
            # identificado pelo ID recebido na URL.
            editar_fornecedor_controller(
                id_fornecedor,
                nome,
                telefone,
                observacao
            )

            # Informa que a atualização foi concluída.
            flash(
                "Fornecedor atualizado com sucesso!",
                "success"
            )

            # Retorna à listagem principal.
            return redirect("/fornecedor")

        # ----------------------------------------------------
        # REQUISIÇÃO GET: ABRIR FORMULÁRIO
        # ----------------------------------------------------
        # Quando a requisição não é POST, busca os dados atuais
        # para preencher o formulário de edição.
        fornecedor = pegar_fornecedor_por_id(
            id_fornecedor
        )

        # Renderiza a página de edição com os dados encontrados.
        return render_template(
            "fornecedor/editar_fornecedor.html",
            fornecedor=fornecedor
        )

    # --------------------------------------------------------
    # LISTAR FORNECEDORES INATIVOS
    # --------------------------------------------------------
    # URL: /fornecedor/inativos
    # Método: GET
    #
    # Busca os fornecedores inativos e exibe a página
    # utilizada para consultar esses registros.
    @app.route("/fornecedor/inativos")
    def fornecedores_inativos():
        """
        Busca e exibe os fornecedores inativos.
        """

        # Solicita ao controller a lista de fornecedores inativos.
        fornecedores = pegar_fornecedores_inativos()

        # Renderiza a página com os dados obtidos.
        return render_template(
            "fornecedor/inativar_fornecedor.html",
            fornecedores=fornecedores
        )

    # --------------------------------------------------------
    # REATIVAR FORNECEDOR
    # --------------------------------------------------------
    # URL: /fornecedor/reativar/<id>
    #
    # Esta rota utiliza try/except para tratar exceções
    # levantadas durante a tentativa de reativação.
    @app.route(
        "/fornecedor/reativar/<int:id>"
    )
    def reativar(id):
        """
        Tenta reativar um fornecedor e informa o resultado.

        Parâmetros:
            id: identificador do fornecedor na URL.
        """

        try:

            # Solicita a reativação do fornecedor.
            reativar_fornecedor(id)

            # Informa que a operação foi concluída.
            flash(
                "Fornecedor reativado com sucesso!",
                "success"
            )

        except Exception:

            # Mantém o comportamento original: se ocorrer
            # uma exceção, exibe uma mensagem genérica.
            flash(
                "Erro ao reativar fornecedor.",
                "danger"
            )

        # Retorna à página de fornecedores inativos.
        return redirect("/fornecedor/inativos")

    # --------------------------------------------------------
    # DESATIVAR FORNECEDOR
    # --------------------------------------------------------
    # URL: /fornecedor/desativar/<id>
    #
    # Tenta desativar o fornecedor selecionado e apresenta
    # uma mensagem de acordo com o resultado da operação.
    @app.route(
        "/fornecedor/desativar/<int:id>"
    )
    def desativar(id):
        """
        Tenta desativar um fornecedor.

        Parâmetros:
            id: identificador do fornecedor na URL.
        """

        try:

            # Solicita ao controller a desativação do fornecedor.
            desativar_fornecedor_controller(id)

            # Informa que a operação foi concluída.
            flash(
                "Fornecedor desativado com sucesso!",
                "success"
            )

        except Exception:

            # Se ocorrer uma exceção, informa que a operação
            # não pôde ser concluída.
            flash(
                "Erro ao desativar fornecedor.",
                "danger"
            )

        # Retorna à listagem principal de fornecedores.
        return redirect("/fornecedor")
