
# ============================================================
# ROTAS DE MOVIMENTAÇÃO DE ESTOQUE — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis por:
#
# - Exibir a tela de movimentação de estoque;
# - Registrar movimentações de produtos;
# - Consultar o histórico de movimentações.
#
# As operações de movimentação são encaminhadas ao controller,
# que contém a lógica responsável por processar os dados.
# ============================================================


# Importa os decorators usados para controlar o acesso.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas necessárias do Flask:
# - render_template: apresenta páginas HTML;
# - request: acessa os dados enviados pelo formulário;
# - redirect: redireciona para outra rota;
# - flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller de movimentação.
#
# A primeira função busca os produtos disponíveis para
# movimentação. A segunda registra uma movimentação.
# A terceira recupera o histórico de movimentações.
from app.controllers.movimentacao_controller import (
    pegar_produtos_movimentacao,
    cadastrar_movimentacao_controller,
    pegar_movimentacoes
)


# ============================================================
# CONFIGURAR ROTAS DE MOVIMENTAÇÃO
# ============================================================
def configurar_movimentacao_routes(app):
    """
    Registra as rotas de movimentação de estoque na aplicação.

    Parâmetros:
        app: instância principal da aplicação Flask.
    """

    # --------------------------------------------------------
    # TELA DE MOVIMENTAÇÃO
    # --------------------------------------------------------
    # URL: /movimentacao
    # Método: GET
    #
    # Busca os produtos necessários para preencher a tela
    # de movimentação de estoque.
    @app.route("/movimentacao")
    @login_obrigatorio
    def movimentacao():
        """
        Exibe a tela de movimentação com os produtos disponíveis.
        """

        # Busca os produtos por meio do controller.
        produtos = pegar_produtos_movimentacao()

        # Renderiza a página e disponibiliza a lista de produtos
        # para o template.
        return render_template(
            "estoque/movimentacao.html",
            produtos=produtos
        )

    # --------------------------------------------------------
    # CADASTRAR MOVIMENTAÇÃO
    # --------------------------------------------------------
    # URL: /movimentacao/cadastrar
    # Método: POST
    #
    # Recebe os dados do formulário e encaminha a operação
    # ao controller de movimentação.
    @app.route(
        "/movimentacao/cadastrar",
        methods=["POST"]
    )
    def cadastrar_movimentacao_route():
        """
        Registra uma movimentação de estoque.

        Os campos de quantidade são convertidos para inteiros.
        Quando estão ausentes ou vazios, utiliza-se zero,
        conforme o comportamento original.
        """

        try:

            # ------------------------------------------------
            # 1. OBTER O PRODUTO
            # ------------------------------------------------
            # Identifica qual produto será movimentado.
            produto_id = request.form.get(
                "produto_id"
            )

            # ------------------------------------------------
            # 2. OBTER O TIPO DE MOVIMENTAÇÃO
            # ------------------------------------------------
            # Recebe o tipo selecionado no formulário.
            # A interpretação desse valor fica a cargo
            # do controller.
            tipo_movimentacao = request.form.get(
                "tipo_movimentacao"
            )

            # ------------------------------------------------
            # 3. OBTER AS QUANTIDADES
            # ------------------------------------------------
            # Obtém a quantidade de caixas.
            #
            # O valor recebido pelo formulário é uma string.
            # Por isso, convertemos para int antes de chamar
            # o controller.
            #
            # Se o campo não existir ou estiver vazio,
            # a expressão utiliza zero.
            quantidade_caixa = int(
                request.form.get(
                    "quantidade_caixa",
                    0
                ) or 0
            )

            # Obtém a quantidade de unidades.
            quantidade_unidade = int(
                request.form.get(
                    "quantidade_unidade",
                    0
                ) or 0
            )

            # Obtém a quantidade fracionada.
            quantidade_fracionada = int(
                request.form.get(
                    "quantidade_fracionada",
                    0
                ) or 0
            )

            # ------------------------------------------------
            # 4. OBTER O MOTIVO
            # ------------------------------------------------
            # Recupera o motivo informado para a movimentação.
            motivo = request.form.get(
                "motivo"
            )

            # ------------------------------------------------
            # 5. ENCAMINHAR AO CONTROLLER
            # ------------------------------------------------
            # Envia os valores na mesma ordem utilizada
            # na chamada original.
            #
            # O controller é responsável por processar a
            # movimentação e encaminhar as alterações
            # necessárias ao model.
            cadastrar_movimentacao_controller(
                produto_id,
                tipo_movimentacao,
                quantidade_caixa,
                quantidade_unidade,
                quantidade_fracionada,
                motivo
            )

            # Se a chamada terminar sem lançar uma exceção,
            # prepara a mensagem de sucesso.
            flash(
                "Movimentação registrada com sucesso!",
                "success"
            )

        except Exception as erro:

            # Se ocorrer uma exceção durante a leitura,
            # conversão ou processamento dos dados, prepara
            # uma mensagem de erro.
            #
            # Mantém o comportamento original de apresentar
            # o texto da exceção na mensagem flash.
            flash(
                str(erro),
                "error"
            )

        # Independentemente do resultado, retorna à página
        # de estoque, conforme o comportamento original.
        return redirect("/estoque")

    # --------------------------------------------------------
    # HISTÓRICO DE MOVIMENTAÇÕES
    # --------------------------------------------------------
    # URL: /movimentacao/historico
    # Método: GET
    #
    # Exibe o histórico das movimentações registradas.
    #
    # Proteção existente:
    # - O usuário precisa estar autenticado;
    # - O perfil deve ser administrador ou gerente.
    @app.route(
        "/movimentacao/historico"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def historico_movimentacao():
        """
        Busca e apresenta o histórico de movimentações.
        """

        # Solicita ao controller todos os registros do histórico.
        movimentacoes = pegar_movimentacoes()

        # Renderiza a página e disponibiliza os registros
        # para o template.
        return render_template(
            "estoque/historico_movimentacao.html",
            movimentacoes=movimentacoes
        )
