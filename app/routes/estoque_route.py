
# ============================================================
# ROTAS DE ESTOQUE — SIGC
# ============================================================
# Este arquivo reúne as rotas relacionadas ao gerenciamento
# de entradas e consultas de estoque.
#
# Funcionalidades:
# - Exibir a página de estoque;
# - Cadastrar entradas de estoque;
# - Consultar o estoque atual;
# - Calcular indicadores de situação do estoque;
# - Consultar os detalhes de um produto e suas informações
# relacionadas ao estoque.
#
# As rotas recebem as requisições do navegador e chamam os
# controllers responsáveis pelas operações do sistema.
# ============================================================


# Importa os decorators utilizados para controlar o acesso.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas do Flask:
# - render_template: exibe páginas HTML;
# - request: acessa os dados enviados pelos formulários;
# - redirect: redireciona para outra rota;
# - flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller de estoque.
from app.controllers.estoque_controller import (
    pegar_estoque,
    cadastrar_estoque_controller,
    pegar_estoque_atual_completo,
    pegar_detalhes_produto_estoque
)

# Importa as funções do controller de produtos.
# Elas fornecem os produtos e as categorias utilizados
# no formulário de entrada de estoque.
from app.controllers.produto_controller import (
    pegar_produtos,
    pegar_categorias
)

# Importa a função que busca os fornecedores disponíveis.
from app.controllers.fornecedor_controller import (
    pegar_fornecedores
)


# ============================================================
# CONFIGURAR ROTAS DE ESTOQUE
# ============================================================
def configurar_estoque_routes(app):
    """
    Registra as rotas de estoque na aplicação Flask.

    Parâmetros:
        app: instância principal da aplicação Flask.

    As rotas são registradas por meio dos decorators
    @app.route dentro desta função.
    """

    # --------------------------------------------------------
    # LISTAR ESTOQUE
    # --------------------------------------------------------
    # URL: /estoque
    # Método: GET
    #
    # Exibe o formulário e os dados necessários para registrar
    # uma entrada de estoque.
    @app.route("/estoque")
    @login_obrigatorio
    def estoque():
        """
        Carrega os produtos, as categorias e os fornecedores
        necessários para exibir a página de estoque.
        """

        # Busca os produtos que serão disponibilizados
        # para seleção na interface.
        produtos = pegar_produtos()

        # Busca as categorias para preencher os filtros
        # ou as opções existentes no template.
        categorias = pegar_categorias()

        # Busca os fornecedores disponíveis para seleção.
        fornecedores = pegar_fornecedores()

        # Renderiza a página de estoque e disponibiliza
        # os dados obtidos pelos controllers.
        return render_template(
            "estoque/estoque.html",
            produtos=produtos,
            categorias=categorias,
            fornecedores=fornecedores
        )

    # --------------------------------------------------------
    # CADASTRAR ENTRADA DE ESTOQUE
    # --------------------------------------------------------
    # URL: /estoque/cadastrar
    # Método: POST
    #
    # Recebe os dados do formulário de entrada e encaminha
    # essas informações ao controller de estoque.
    @app.route(
        "/estoque/cadastrar",
        methods=["POST"]
    )
    def cadastrar_estoque_route():
        """
        Recebe os dados de uma entrada de estoque.

        A rota coleta os valores do formulário e os encaminha
        ao controller, que executa a operação correspondente.
        """

        # ----------------------------------------------------
        # 1. IDENTIFICAR O PRODUTO
        # ----------------------------------------------------
        # Obtém o ID do produto que receberá a entrada.
        produto_id = request.form.get(
            "produto_id"
        )

        # ----------------------------------------------------
        # 2. IDENTIFICAR A ORIGEM DA COMPRA
        # ----------------------------------------------------
        # Obtém o ID da origem de compra selecionada.
        origem_compra_id = request.form.get(
            "origem_compra_id"
        )

        # Obtém o nome do local de origem, quando informado.
        nome_origem = request.form.get(
            "nome_origem"
        )

        # ----------------------------------------------------
        # 3. IDENTIFICAR O FORNECEDOR
        # ----------------------------------------------------
        # Obtém o ID do fornecedor selecionado no formulário.
        fornecedor_id = request.form.get(
            "fornecedor_id"
        )

        # Quando o formulário envia uma string vazia,
        # converte o valor para None.
        #
        # Isso permite indicar a ausência de fornecedor,
        # desde que o controller e o banco aceitem esse valor.
        if fornecedor_id == "":
            fornecedor_id = None

        # ----------------------------------------------------
        # 4. OBTER O TIPO DE ENTRADA
        # ----------------------------------------------------
        # Registra o tipo de entrada selecionado no formulário.
        tipo_entrada = request.form.get(
            "tipo_entrada"
        )

        # ----------------------------------------------------
        # 5. OBTER AS QUANTIDADES RECEBIDAS
        # ----------------------------------------------------
        # Quantidade de caixas recebidas.
        quantidade_recebida_caixa = request.form.get(
            "quantidade_recebida_caixa"
        )

        # Quantidade de unidades recebidas separadamente.
        quantidade_recebida_unidade = request.form.get(
            "quantidade_recebida_unidade"
        )

        # ----------------------------------------------------
        # 6. OBTER O VALOR E A DATA DA COMPRA
        # ----------------------------------------------------
        # Valor total informado para a compra.
        preco_total_compra = request.form.get(
            "preco_total_compra"
        )

        # Data em que a entrada ocorreu.
        data_entrada = request.form.get(
            "data_entrada"
        )

        # ----------------------------------------------------
        # 7. ENCAMINHAR OS DADOS AO CONTROLLER
        # ----------------------------------------------------
        # A rota não executa diretamente a gravação no banco.
        # Ela entrega os valores ao controller, preservando
        # a separação entre as camadas da aplicação.
        #
        # A ordem dos argumentos é mantida conforme a chamada
        # existente no código original.
        cadastrar_estoque_controller(
            produto_id,
            origem_compra_id,
            nome_origem,
            fornecedor_id,
            tipo_entrada,
            quantidade_recebida_caixa,
            quantidade_recebida_unidade,
            preco_total_compra,
            data_entrada
        )

        # Prepara uma mensagem de sucesso para a interface.
        flash(
            "Entrada de estoque registrada com sucesso!",
            "success"
        )

        # Redireciona para a página de estoque.
        return redirect("/estoque")

    # --------------------------------------------------------
    # CONSULTAR ESTOQUE ATUAL
    # --------------------------------------------------------
    # URL: /estoque/atual
    # Método: GET
    #
    # Exibe o estoque atual e os indicadores que resumem
    # a situação dos produtos.
    #
    # Proteção existente:
    # - Usuário autenticado;
    # - Perfil administrador ou gerente.
    @app.route("/estoque/atual")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def estoque_atual():
        """
        Busca o estoque atual e calcula os indicadores.

        Os indicadores são contagens de produtos classificados
        conforme o valor de status_estoque retornado pelo
        controller.
        """

        # Busca os registros de estoque com os dados necessários
        # para apresentar a página de estoque atual.
        estoque = pegar_estoque_atual_completo()

        # Conta quantos registros foram retornados.
        # Essa contagem representa o total de itens da lista
        # retornada pelo controller.
        total_produtos = len(estoque)

        # Inicializa os indicadores em zero.
        # Cada contador será incrementado conforme o status
        # encontrado nos registros de estoque.
        total_em_estoque = 0
        total_baixo = 0
        total_sem_estoque = 0
        total_nunca_abastecido = 0
        total_minimo = 0

        # Percorre todos os registros para classificar
        # cada item de acordo com seu status_estoque.
        for item in estoque:

            # Obtém o status atribuído ao registro.
            status = item["status_estoque"]

            # Estoque classificado como normal.
            if status == "normal":
                total_em_estoque += 1

            # Estoque classificado como mínimo.
            elif status == "minimo":
                total_minimo += 1

            # Estoque classificado como baixo.
            elif status == "baixo":
                total_baixo += 1

            # Produto classificado como sem estoque.
            elif status == "sem_estoque":
                total_sem_estoque += 1

            # Produto que nunca recebeu abastecimento.
            elif status == "nunca_abastecido":
                total_nunca_abastecido += 1

        # Envia os registros e os indicadores para o template.
        return render_template(
            "estoque/estoque_atual.html",
            estoque=estoque,
            total_produtos=total_produtos,
            total_em_estoque=total_em_estoque,
            total_minimo=total_minimo,
            total_baixo=total_baixo,
            total_sem_estoque=total_sem_estoque,
            total_nunca_abastecido=total_nunca_abastecido
        )

    # --------------------------------------------------------
    # DETALHES DO PRODUTO NO ESTOQUE
    # --------------------------------------------------------
    # URL: /estoque/produto/<produto_id>
    # Método: GET
    #
    # Busca os detalhes de um produto e os encaminha
    # para a página específica de consulta.
    @app.route(
        "/estoque/produto/<int:produto_id>"
    )
    def detalhes_produto(produto_id):
        """
        Busca e apresenta os detalhes de um produto no estoque.

        Parâmetros:
            produto_id: ID do produto recebido pela URL.
        """

        # Solicita ao controller os detalhes do produto
        # e as informações relacionadas ao estoque.
        produto = pegar_detalhes_produto_estoque(
            produto_id
        )

        # Renderiza a página de detalhes.
        return render_template(
            "estoque/detalhes_produto.html",
            produto=produto
        )
