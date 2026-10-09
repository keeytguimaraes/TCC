
# ============================================================
# ROTAS DE AUTENTICAÇÃO — SIGC
# ============================================================
# Este arquivo controla as rotas responsáveis por:
#
# - Exibir a tela de login;
# - Receber o usuário e a senha enviados pelo formulário;
# - Solicitar a autenticação ao auth_controller;
# - Armazenar os dados do usuário autenticado na sessão;
# - Redirecionar o usuário para o dashboard;
# - Encerrar a sessão ao realizar logout.
#
# IMPORTANTE:
# As regras de validação das credenciais ficam no controller.
# Este arquivo recebe as requisições HTTP e define o que
# acontece antes e depois da autenticação.
# ============================================================


# Importa as ferramentas necessárias para trabalhar com
# requisições, páginas HTML, sessões e mensagens do Flask.
from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

# Importa a função responsável por verificar as credenciais.
# A rota não precisa conhecer os detalhes internos dessa
# validação: ela apenas chama o controller e recebe o resultado.
from app.controllers.auth_controller import (
    autenticar_usuario
)


# ============================================================
# CONFIGURAR ROTAS DE AUTENTICAÇÃO
# ============================================================
def configurar_auth_routes(app):
    """
    Registra as rotas de autenticação na aplicação Flask.

    Parâmetros:
        app: instância principal da aplicação Flask.

    Esta função recebe a aplicação e registra nela as rotas
    de login e logout por meio dos decorators @app.route.
    """

    # --------------------------------------------------------
    # ROTA DE LOGIN
    # --------------------------------------------------------
    # URL: /login
    #
    # GET:
    # Exibe a página de login.
    #
    # POST:
    # Recebe os dados preenchidos pelo usuário e tenta
    # realizar a autenticação.
    @app.route(
        "/login",
        methods=["GET", "POST"]
    )
    def login():
        """
        Exibe a tela de login e processa a autenticação.

        Se a requisição for GET, apresenta o formulário.
        Se for POST, envia as credenciais ao controller.

        Quando a autenticação é bem-sucedida, os dados básicos
        do usuário são armazenados na sessão e ocorre o
        redirecionamento para o dashboard.

        Se a autenticação falhar, uma mensagem é exibida.
        """

        # Verifica se o formulário foi enviado.
        if request.method == "POST":

            # Obtém o nome de usuário enviado pelo formulário.
            #
            # O método get() retorna None caso o campo não
            # exista na requisição.
            usuario = request.form.get(
                "usuario"
            )

            # Obtém a senha enviada pelo formulário.
            senha = request.form.get(
                "senha"
            )

            # Solicita ao controller que valide as credenciais.
            #
            # O controller retorna os dados do usuário quando
            # a autenticação é bem-sucedida ou um resultado
            # falso quando as credenciais não são válidas.
            usuario_logado = (
                autenticar_usuario(
                    usuario,
                    senha
                )
            )

            # Se o controller retornar um usuário válido,
            # inicia o armazenamento dos dados na sessão.
            if usuario_logado:

                # Guarda o ID do usuário autenticado.
                # Esse valor pode ser utilizado por outras
                # rotas e controllers para identificar o usuário.
                session["usuario_id"] = (
                    usuario_logado["id"]
                )

                # Guarda o nome do usuário para uso em telas
                # e outras partes do sistema.
                session["nome"] = (
                    usuario_logado["nome"]
                )

                # Guarda o perfil de acesso do usuário.
                # Outras partes da aplicação podem utilizar
                # essa informação para verificar permissões.
                session["perfil"] = (
                    usuario_logado["perfil"]
                )

                # Redireciona o usuário autenticado para
                # a página principal do dashboard.
                return redirect("/dashboard")

            # Se a autenticação falhar, registra uma mensagem
            # temporária que poderá ser exibida no template.
            #
            # A categoria "error" permite que o HTML diferencie
            # visualmente essa mensagem de outros avisos.
            flash(
                "Usuário ou senha inválidos",
                "error"
            )

        # Se a requisição for GET ou se a autenticação falhar,
        # exibe a página de login.
        #
        # Neste último caso, a mensagem criada por flash()
        # poderá ser apresentada pelo template.
        return render_template(
            "auth/login.html"
        )

    # --------------------------------------------------------
    # ROTA DE LOGOUT
    # --------------------------------------------------------
    # URL: /logout
    #
    # Esta rota encerra a sessão atual e redireciona
    # o usuário para a página de login.
    @app.route("/logout")
    def logout():
        """
        Encerra a sessão atual do usuário.

        session.clear() remove os dados armazenados na sessão,
        incluindo usuario_id, nome e perfil.

        Em seguida, redireciona para a tela de login.
        """

        # Remove todos os dados da sessão atual.
        session.clear()

        # Retorna o usuário para a tela de login.
        return redirect("/login")
