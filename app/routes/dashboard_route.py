
# ============================================================
# ROTAS DO DASHBOARD — SIGC
# ============================================================
# Este arquivo contém as rotas responsáveis por apresentar
# o dashboard principal do Sistema Integrado de Gestão Comercial.
#
# Funcionalidades:
# - Verificar se o usuário está autenticado;
# - Buscar os dados do dashboard por meio do controller;
# - Identificar o perfil do usuário na sessão;
# - Enviar os dados para o template HTML.
#
# O cálculo dos indicadores e a consulta das informações
# ficam sob responsabilidade do dashboard_controller e
# das camadas inferiores do sistema.
# ============================================================


# Importa render_template para exibir uma página HTML.
# Importa session para acessar os dados da sessão atual.
from flask import (
    render_template,
    session
)

# Importa o decorator que exige autenticação.
# Ele protege a rota para que somente usuários autenticados
# possam acessá-la, conforme a implementação desse decorator.
from app.utils.auth import (
    login_obrigatorio
)

# Importa a função que obtém os dados do dashboard.
from app.controllers.dashboard_controller import (
    pegar_dashboard
)


# ============================================================
# CONFIGURAR ROTAS DO DASHBOARD
# ============================================================
def configurar_dashboard_routes(app):
    """
    Registra as rotas do dashboard na aplicação Flask.

    Parâmetros:
        app: instância principal da aplicação Flask.

    A função registra a rota /dashboard, responsável por
    carregar os indicadores e apresentar a página principal.
    """

    # --------------------------------------------------------
    # ROTA PRINCIPAL DO DASHBOARD
    # --------------------------------------------------------
    # URL: /dashboard
    # Método: GET
    #
    # O decorator login_obrigatorio exige que o usuário esteja
    # autenticado antes de acessar a página.
    @app.route("/dashboard")
    @login_obrigatorio
    def dashboard():
        """
        Carrega os dados do dashboard e exibe a página.

        Fluxo:
        1. Busca os indicadores pelo controller.
        2. Obtém o perfil armazenado na sessão.
        3. Renderiza o template com os dados encontrados.
        """

        # Solicita ao controller os dados necessários para
        # montar o dashboard.
        #
        # A função pode retornar indicadores, totais, gráficos
        # e outras informações definidas na implementação
        # de pegar_dashboard().
        dados = pegar_dashboard()

        # Obtém o perfil do usuário autenticado.
        #
        # O método get() retorna None se a chave "perfil"
        # não estiver presente na sessão.
        #
        # O template pode utilizar essa informação para
        # apresentar conteúdos de acordo com o perfil.
        perfil = session.get(
            "perfil"
        )

        # Renderiza o template do dashboard.
        #
        # dados: informações retornadas pelo controller.
        # perfil: perfil do usuário armazenado na sessão.
        return render_template(
            "dashboard/dashboard.html",
            dados=dados,
            perfil=perfil
        )
