
# ============================================================
# ROTAS DE USUÁRIOS — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis pelo gerenciamento
# dos usuários que podem acessar o sistema.
#
# Funcionalidades:
# - Listar usuários;
# - Exibir o formulário de cadastro;
# - Cadastrar usuários;
# - Exibir o formulário de edição;
# - Atualizar dados de usuários;
# - Desativar usuários;
# - Listar usuários inativos;
# - Reativar usuários;
# - Exibir o formulário de alteração de senha;
# - Alterar a senha de um usuário.
#
# As operações de consulta e alteração são encaminhadas
# ao controller de usuários.
#
# As rotas administrativas exigem autenticação e o perfil
# de administrador, conforme definido originalmente.
# ============================================================


# Importa as ferramentas utilizadas nas rotas Flask.
from flask import (
    render_template,
    request,
    redirect,
    flash,
    session
)

# Importa as funções do controller responsáveis por
# consultar, cadastrar, editar, desativar, reativar
# e alterar usuários.
from app.controllers.usuario_controller import (
    pegar_usuarios,
    cadastrar_usuario_controller,
    usuario_existe,
    buscar_usuario_controller,
    editar_usuario_controller,
    desativar_usuario_controller,
    listar_usuarios_inativos_controller,
    reativar_usuario_controller,
    alterar_senha_usuario_controller
)

# Importa os decorators responsáveis por exigir login
# e restringir o acesso de acordo com o perfil do usuário.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)


# ============================================================
# CONFIGURAR ROTAS DE USUÁRIOS
# ============================================================
def configurar_usuario_routes(app):
    """
    Registra as rotas de gerenciamento de usuários.

    Parâmetros:
        app: instância principal da aplicação Flask.
    """

    # --------------------------------------------------------
    # LISTAR USUÁRIOS
    # --------------------------------------------------------
    # URL: /usuario
    # Método: GET
    #
    # Exige que o usuário esteja autenticado e tenha
    # o perfil de administrador.
    @app.route("/usuario")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def usuario():
        """
        Busca e apresenta a lista de usuários cadastrados.
        """

        # Solicita ao controller os dados dos usuários.
        dados = pegar_usuarios()

        # Abre a página de listagem e disponibiliza os dados
        # por meio da variável 'usuarios'.
        return render_template(
            "usuario/usuario.html",
            usuarios=dados
        )

    # --------------------------------------------------------
    # EXIBIR FORMULÁRIO DE CADASTRO
    # --------------------------------------------------------
    # URL: /usuario/cadastrar
    # Método: GET
    #
    # Apresenta o formulário para cadastrar um novo usuário.
    @app.route(
        "/usuario/cadastrar"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def tela_cadastrar_usuario():
        """
        Exibe a página de cadastro de usuários.
        """

        # Renderiza o formulário de cadastro.
        return render_template(
            "usuario/cadastrar_usuario.html"
        )

    # --------------------------------------------------------
    # CADASTRAR USUÁRIO
    # --------------------------------------------------------
    # URL: /usuario/cadastrar
    # Método: POST
    #
    # Recebe os dados do formulário, verifica se o login
    # já existe e confirma se as senhas são iguais.
    @app.route(
        "/usuario/cadastrar",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def cadastrar_usuario():
        """
        Valida os dados e solicita o cadastro de um usuário.
        """

        # ----------------------------------------------------
        # 1. RECUPERAR OS DADOS BÁSICOS
        # ----------------------------------------------------
        # Obtém o nome informado no formulário.
        nome = request.form.get(
            "nome"
        )

        # Obtém o login que será utilizado pelo novo usuário.
        usuario = request.form.get(
            "usuario"
        )

        # ----------------------------------------------------
        # 2. VERIFICAR SE O LOGIN JÁ EXISTE
        # ----------------------------------------------------
        # Consulta o controller para verificar se já existe
        # um usuário com o login informado.
        if usuario_existe(usuario):

            # Informa que o login não pode ser reutilizado.
            flash(
                "Já existe um usuário com esse login.",
                "error"
            )

            # Retorna ao formulário para que o administrador
            # possa corrigir o login informado.
            return redirect(
                "/usuario/cadastrar"
            )

        # ----------------------------------------------------
        # 3. RECUPERAR E VALIDAR AS SENHAS
        # ----------------------------------------------------
        # Obtém a senha digitada pelo administrador.
        senha = request.form.get(
            "senha"
        )

        # Obtém a confirmação da senha.
        confirmar_senha = request.form.get(
            "confirmar_senha"
        )

        # Recupera o perfil atribuído ao novo usuário.
        perfil = request.form.get(
            "perfil"
        )

        # Compara a senha com sua confirmação.
        # Se forem diferentes, interrompe o cadastro.
        if senha != confirmar_senha:

            # Exibe uma mensagem para informar o problema.
            flash(
                "As senhas não coincidem.",
                "error"
            )

            # Retorna ao formulário sem chamar o controller
            # de cadastro.
            return redirect(
                "/usuario/cadastrar"
            )

        # ----------------------------------------------------
        # 4. CADASTRAR O USUÁRIO
        # ----------------------------------------------------
        # Se as validações anteriores forem aprovadas,
        # encaminha os dados ao controller.
        #
        # A ordem dos argumentos é mantida conforme
        # a implementação original.
        cadastrar_usuario_controller(
            nome,
            usuario,
            senha,
            perfil
        )

        # Informa que a chamada de cadastro foi concluída.
        flash(
            "Usuário cadastrado com sucesso!",
            "success"
        )

        # Retorna à listagem de usuários.
        return redirect(
            "/usuario"
        )

    # --------------------------------------------------------
    # EXIBIR FORMULÁRIO DE EDIÇÃO
    # --------------------------------------------------------
    # URL: /usuario/editar/<id_usuario>
    # Método: GET
    #
    # O ID recebido pela URL identifica o usuário que será
    # carregado no formulário de edição.
    @app.route(
        "/usuario/editar/<int:id_usuario>"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def tela_editar_usuario(id_usuario):
        """
        Busca os dados de um usuário para exibir na edição.
        """

        # Busca o usuário pelo identificador recebido na URL.
        usuario = buscar_usuario_controller(
            id_usuario
        )

        # Renderiza o formulário e envia os dados encontrados.
        return render_template(
            "usuario/editar_usuario.html",
            usuario=usuario
        )

    # --------------------------------------------------------
    # ATUALIZAR DADOS DO USUÁRIO
    # --------------------------------------------------------
    # URL: /usuario/editar/<id_usuario>
    # Método: POST
    #
    # Recebe os novos dados e solicita a atualização
    # do usuário correspondente.
    @app.route(
        "/usuario/editar/<int:id_usuario>",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def editar_usuario(id_usuario):
        """
        Atualiza o nome, o login e o perfil de um usuário.
        """

        # Recupera o novo nome informado no formulário.
        nome = request.form.get(
            "nome"
        )

        # Recupera o novo login.
        usuario = request.form.get(
            "usuario"
        )

        # Recupera o perfil selecionado.
        perfil = request.form.get(
            "perfil"
        )

        # Encaminha o identificador e os novos dados
        # ao controller responsável pela atualização.
        editar_usuario_controller(
            id_usuario,
            nome,
            usuario,
            perfil
        )

        # Informa que a chamada de atualização foi concluída.
        flash(
            "Usuário atualizado com sucesso!",
            "success"
        )

        # Retorna à listagem de usuários.
        return redirect(
            "/usuario"
        )

    # --------------------------------------------------------
    # DESATIVAR USUÁRIO
    # --------------------------------------------------------
    # URL: /usuario/desativar/<id_usuario>
    # Método: POST
    #
    # Além da autenticação e do perfil administrativo,
    # verifica se o administrador está tentando desativar
    # a própria conta.
    @app.route(
        "/usuario/desativar/<int:id_usuario>",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def desativar_usuario(id_usuario):
        """
        Desativa um usuário, impedindo a desativação
        da própria conta pela rota.
        """

        # ----------------------------------------------------
        # 1. VERIFICAR SE O USUÁRIO ESTÁ DESATIVANDO A SI MESMO
        # ----------------------------------------------------
        # session["usuario_id"] contém o ID do usuário
        # autenticado, conforme a implementação da sessão.
        #
        # Se o ID da URL for igual ao ID da sessão, significa
        # que o administrador está tentando desativar a
        # própria conta.
        if id_usuario == session["usuario_id"]:

            # Informa que essa operação não é permitida.
            flash(
                "Você não pode desativar seu próprio usuário.",
                "error"
            )

            # Interrompe a operação e retorna à listagem.
            return redirect(
                "/usuario"
            )

        # ----------------------------------------------------
        # 2. SOLICITAR A DESATIVAÇÃO
        # ----------------------------------------------------
        # A operação é encaminhada ao controller.
        desativar_usuario_controller(
            id_usuario
        )

        # Informa que a chamada de desativação foi concluída.
        flash(
            "Usuário desativado com sucesso!",
            "success"
        )

        # Retorna à listagem de usuários ativos.
        return redirect(
            "/usuario"
        )

    # --------------------------------------------------------
    # LISTAR USUÁRIOS INATIVOS
    # --------------------------------------------------------
    # URL: /usuario/inativos
    # Método: GET
    #
    # Exibe os usuários que estão inativos.
    @app.route(
        "/usuario/inativos"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def usuarios_inativos():
        """
        Busca e apresenta os usuários inativos.
        """

        # Busca os registros por meio do controller.
        dados = listar_usuarios_inativos_controller()

        # Abre a página de usuários inativos e envia
        # os registros usando a variável 'usuarios'.
        return render_template(
            "usuario/usuarios_inativos.html",
            usuarios=dados
        )

    # --------------------------------------------------------
    # REATIVAR USUÁRIO
    # --------------------------------------------------------
    # URL: /usuario/reativar/<id_usuario>
    # Método: POST
    #
    # Solicita a reativação de um usuário anteriormente
    # desativado.
    @app.route(
        "/usuario/reativar/<int:id_usuario>",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def reativar_usuario(id_usuario):
        """
        Reativa um usuário e retorna à lista de inativos.
        """

        # Encaminha o ID ao controller responsável pela
        # reativação.
        reativar_usuario_controller(
            id_usuario
        )

        # Informa que a chamada de reativação foi concluída.
        flash(
            "Usuário reativado com sucesso!",
            "success"
        )

        # Retorna à página de usuários inativos.
        return redirect(
            "/usuario/inativos"
        )

    # --------------------------------------------------------
    # EXIBIR FORMULÁRIO DE ALTERAÇÃO DE SENHA
    # --------------------------------------------------------
    # URL: /usuario/senha/<id_usuario>
    # Método: GET
    #
    # Busca o usuário e apresenta o formulário de alteração
    # de senha.
    @app.route(
        "/usuario/senha/<int:id_usuario>"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def tela_alterar_senha(id_usuario):
        """
        Exibe a página de alteração de senha de um usuário.
        """

        # Busca os dados do usuário pelo ID.
        usuario = buscar_usuario_controller(
            id_usuario
        )

        # Renderiza o formulário e envia os dados do usuário.
        return render_template(
            "usuario/alterar_senha.html",
            usuario=usuario
        )

    # --------------------------------------------------------
    # ALTERAR SENHA
    # --------------------------------------------------------
    # URL: /usuario/senha/<id_usuario>
    # Método: POST
    #
    # Recebe a nova senha e sua confirmação.
    # A alteração só é solicitada quando os valores coincidem.
    @app.route(
        "/usuario/senha/<int:id_usuario>",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def alterar_senha(id_usuario):
        """
        Valida a confirmação da senha e solicita sua alteração.
        """

        # Recupera a nova senha.
        senha = request.form.get(
            "senha"
        )

        # Recupera a confirmação da nova senha.
        confirmar_senha = request.form.get(
            "confirmar_senha"
        )

        # ----------------------------------------------------
        # 1. VALIDAR A CONFIRMAÇÃO
        # ----------------------------------------------------
        # Se os valores forem diferentes, não solicita
        # a alteração ao controller.
        if senha != confirmar_senha:

            # Informa que as senhas não coincidem.
            flash(
                "As senhas não coincidem.",
                "error"
            )

            # Retorna ao formulário do usuário correspondente.
            return redirect(
                f"/usuario/senha/{id_usuario}"
            )

        # ----------------------------------------------------
        # 2. SOLICITAR A ALTERAÇÃO DA SENHA
        # ----------------------------------------------------
        # Encaminha o ID e a nova senha ao controller.
        # O processamento da senha é responsabilidade
        # da camada de controle e do model correspondente.
        alterar_senha_usuario_controller(
            id_usuario,
            senha
        )

        # Informa que a chamada de alteração foi concluída.
        flash(
            "Senha alterada com sucesso!",
            "success"
        )

        # Retorna à listagem de usuários.
        return redirect(
            "/usuario"
        )
