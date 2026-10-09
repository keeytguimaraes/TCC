
# ============================================================
# ROTAS DA SINUCA — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis por:
#
# - Exibir a tela de configuração da sinuca;
# - Consultar a configuração atual;
# - Apresentar os dados do relatório da sinuca;
# - Salvar alterações nas configurações.
#
# As operações de consulta e gravação são encaminhadas
# ao controller de sinuca.
# ============================================================


# Importa os decorators responsáveis pelo controle de acesso.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas utilizadas pelas rotas Flask.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller da sinuca.
from app.controllers.sinuca_controller import (
    pegar_config_sinuca,
    salvar_config_sinuca,
    pegar_dados_relatorio_sinuca
)


# ============================================================
# CONFIGURAR ROTAS DA SINUCA
# ============================================================
def configurar_sinuca_routes(app):
    """
    Registra as rotas de configuração da sinuca na aplicação.

    Parâmetros:
        app: instância principal da aplicação Flask.
    """

    # --------------------------------------------------------
    # TELA DE CONFIGURAÇÃO DA SINUCA
    # --------------------------------------------------------
    # URL: /sinuca
    # Método: GET
    #
    # Exige autenticação e perfil de administrador ou gerente.
    #
    # Busca as configurações atuais e os dados do relatório
    # para exibi-los na página.
    @app.route("/sinuca")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def sinuca():
        """
        Exibe as configurações e os dados do relatório da sinuca.
        """

        # Busca as configurações atuais da sinuca.
        # Esses dados podem incluir o nome, o valor da ficha
        # e o percentual destinado ao comércio.
        config = pegar_config_sinuca()

        # Busca os dados utilizados no relatório da sinuca.
        dados = pegar_dados_relatorio_sinuca()

        # Renderiza a página e envia as duas informações
        # para o template.
        return render_template(
            "sinuca/configuracao_sinuca.html",
            config=config,
            dados=dados
        )

    # --------------------------------------------------------
    # SALVAR CONFIGURAÇÃO DA SINUCA
    # --------------------------------------------------------
    # URL: /sinuca/salvar
    # Método: POST
    #
    # Recebe os valores enviados pelo formulário e os encaminha
    # ao controller para salvar as configurações.
    @app.route(
        "/sinuca/salvar",
        methods=["POST"]
    )
    def salvar_sinuca():
        """
        Recebe e salva os dados de configuração da sinuca.
        """

        # Recupera o nome informado no formulário.
        nome = request.form.get(
            "nome"
        )

        # Recupera o valor de cada ficha.
        valor_ficha = request.form.get(
            "valor_ficha"
        )

        # Recupera o percentual destinado ao comércio.
        percentual_comercio = request.form.get(
            "percentual_comercio"
        )

        # Encaminha os valores ao controller.
        # A ordem dos argumentos é mantida conforme o código
        # original para preservar a compatibilidade.
        salvar_config_sinuca(
            nome,
            valor_ficha,
            percentual_comercio
        )

        # Informa que a configuração foi atualizada.
        flash(
            "Configuração atualizada com sucesso!",
            "success"
        )

        # Retorna à tela de configuração da sinuca.
        return redirect(
            "/sinuca"
        )
