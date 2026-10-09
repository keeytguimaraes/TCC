
# ============================================================
# ROTAS DE VENDAS — SIGC
# ============================================================
# Este arquivo reúne as rotas relacionadas ao módulo de vendas.
#
# Funcionalidades:
# - Exibir a tela de vendas;
# - Cadastrar uma venda diretamente;
# - Adicionar produtos ao carrinho;
# - Consultar o estoque antes de adicionar um produto;
# - Calcular preços e subtotais;
# - Agrupar itens iguais no carrinho;
# - Exibir o histórico de vendas;
# - Exibir os detalhes de uma venda;
# - Adicionar fichas de sinuca ao carrinho.
#
# Os controllers são responsáveis por encaminhar as operações
# às camadas de negócio e aos models correspondentes.
#
# IMPORTANTE:
# As regras de preços, estoque e montagem do carrinho foram
# mantidas conforme a implementação original.
# ============================================================


# ------------------------------------------------------------
# IMPORTAÇÕES DO FLASK
# ------------------------------------------------------------
# render_template: renderiza páginas HTML.
# request: recupera os dados enviados pelos formulários.
# redirect: redireciona o navegador para outra rota.
# session: armazena dados associados à sessão do usuário,
#          incluindo o carrinho de compras.
# flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

# ------------------------------------------------------------
# AUTENTICAÇÃO E CONTROLE DE ACESSO
# ------------------------------------------------------------
# login_obrigatorio exige que o usuário esteja autenticado.
# perfil_obrigatorio restringe o acesso aos perfis informados.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# ------------------------------------------------------------
# CONTROLLER DE VENDAS
# ------------------------------------------------------------
# pegar_historico_vendas: consulta o histórico de vendas.
# cadastrar_venda_controller: processa o cadastro direto
#                             de uma venda.
# pegar_detalhes_venda: recupera os produtos de uma venda.
from app.controllers.vendas_controller import (
    pegar_historico_vendas,
    cadastrar_venda_controller,
    pegar_detalhes_venda
)

# ------------------------------------------------------------
# CONTROLLER DE PRODUTOS
# ------------------------------------------------------------
# pegar_produtos_venda: recupera os produtos disponíveis
#                       para a tela de vendas.
# pegar_categorias: recupera as categorias para os filtros.
from app.controllers.produto_controller import (
    pegar_produtos_venda,
    pegar_categorias
)

# ------------------------------------------------------------
# CONTROLLER DE CLIENTES
# ------------------------------------------------------------
# Recupera os clientes que serão apresentados na tela de vendas.
from app.controllers.cliente_controller import (
    pegar_clientes
)

# ------------------------------------------------------------
# CONTROLLER DE ESTOQUE
# ------------------------------------------------------------
# Consulta o estoque atual de um produto para verificar
# se existe quantidade suficiente para a venda.
from app.controllers.estoque_controller import (
    pegar_estoque_atual
)

# ------------------------------------------------------------
# CONTROLLER DE SINUCA
# ------------------------------------------------------------
# pegar_config_sinuca: recupera as configurações da sinuca.
# adicionar_ficha_carrinho: adiciona fichas ao carrinho.
# buscar_fichas_venda: recupera as fichas de uma venda.
from app.controllers.sinuca_controller import (
    pegar_config_sinuca,
    adicionar_ficha_carrinho,
    buscar_fichas_venda
)


# ============================================================
# CONFIGURAR ROTAS DE VENDAS
# ============================================================
def configurar_venda_routes(app):
    """
    Registra as rotas relacionadas ao módulo de vendas.

    Parâmetros:
        app: instância principal da aplicação Flask.
    """

    # --------------------------------------------------------
    # TELA PRINCIPAL DE VENDAS
    # --------------------------------------------------------
    # URL: /venda
    # Método: GET
    #
    # Busca os dados necessários para montar a tela de vendas,
    # recupera o carrinho da sessão e calcula o total atual.
    @app.route("/venda")
    @login_obrigatorio
    def venda():
        """
        Exibe os produtos, os clientes, as categorias,
        as configurações da sinuca e o carrinho atual.
        """

        # Mantém a lista de vendas vazia, conforme o código
        # original. A variável é enviada ao template.
        vendas = []

        # Recupera os produtos disponíveis para venda.
        produtos = pegar_produtos_venda()

        # Recupera as categorias utilizadas na interface.
        categorias = pegar_categorias()

        # Recupera os clientes cadastrados.
        clientes = pegar_clientes()

        # Recupera as configurações da sinuca.
        config_sinuca = pegar_config_sinuca()

        # Recupera o carrinho salvo na sessão.
        # Se ainda não existir, utiliza uma lista vazia.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Inicializa o total do carrinho.
        total_carrinho = 0

        # Percorre os itens do carrinho e soma seus subtotais.
        for item in carrinho:
            total_carrinho += item["subtotal"]

        # Inicializa a quantidade de fichas de sinuca.
        quantidade_fichas = 0

        # Procura no carrinho um item identificado como sinuca.
        for item in carrinho:

            # Verifica o tipo do item antes de acessar
            # a quantidade de fichas.
            if item.get("tipo_item") == "sinuca":

                # Recupera a quantidade do primeiro item
                # de sinuca encontrado.
                quantidade_fichas = item["quantidade"]

                # Interrompe a busca após encontrar o item.
                break

        # Renderiza a tela principal de vendas e envia
        # todas as informações necessárias ao template.
        return render_template(
            "venda/venda.html",
            vendas=vendas,
            produtos=produtos,
            categorias=categorias,
            clientes=clientes,
            carrinho=carrinho,
            total_carrinho=total_carrinho,
            config_sinuca=config_sinuca,
            quantidade_fichas=quantidade_fichas
        )

    # --------------------------------------------------------
    # CADASTRAR VENDA DIRETAMENTE
    # --------------------------------------------------------
    # URL: /venda/cadastrar
    # Método: POST
    #
    # Recebe os dados de uma venda e os encaminha diretamente
    # ao controller de vendas.
    @app.route(
        "/venda/cadastrar",
        methods=["POST"]
    )
    def cadastrar_venda_route():
        """
        Recebe os dados do formulário e solicita o cadastro
        de uma venda ao controller.
        """

        # Recupera o identificador do produto selecionado.
        produto_id = request.form.get(
            "produto_id"
        )

        # Recupera a quantidade informada no formulário.
        quantidade = request.form.get(
            "quantidade"
        )

        # Recupera o tipo de venda selecionado.
        tipo_venda = request.form.get(
            "tipo_venda"
        )

        # Recupera o valor recebido do cliente.
        valor_recebido = request.form.get(
            "valor_recebido"
        )

        # Recupera o status de pagamento informado.
        status_pagamento = request.form.get(
            "status_pagamento"
        )

        # Encaminha os dados ao controller na mesma ordem
        # utilizada originalmente.
        cadastrar_venda_controller(
            produto_id,
            quantidade,
            tipo_venda,
            valor_recebido,
            status_pagamento
        )

        # Retorna à tela principal de vendas.
        return redirect(
            "/venda"
        )

    # --------------------------------------------------------
    # ADICIONAR PRODUTO AO CARRINHO
    # --------------------------------------------------------
    # URL: /carrinho/adicionar
    # Método: POST
    #
    # Esta rota:
    # 1. Recupera o produto e o tipo de venda;
    # 2. Localiza o produto no catálogo;
    # 3. Consulta o estoque;
    # 4. Calcula o preço unitário;
    # 5. Calcula o subtotal;
    # 6. Agrupa o produto com um item equivalente ou cria
    #    um novo item no carrinho;
    # 7. Salva o carrinho na sessão.
    @app.route(
        "/carrinho/adicionar",
        methods=["POST"]
    )
    def adicionar_carrinho():
        """
        Adiciona um produto ao carrinho de vendas.
        """

        # ----------------------------------------------------
        # 1. RECUPERAR OS DADOS DO FORMULÁRIO
        # ----------------------------------------------------

        # Recupera o ID do produto selecionado.
        # O valor é normalmente recebido como string.
        produto_id = request.form.get(
            "produto_id"
        )

        # Recupera o tipo de venda e remove espaços no começo
        # e no final do texto.
        #
        # O método strip() pressupõe que o campo foi enviado.
        tipo_venda = request.form.get(
            "tipo_venda"
        ).strip()

        # Recupera a quantidade e converte o valor para inteiro.
        quantidade = int(
            request.form.get(
                "quantidade"
            )
        )

        # ----------------------------------------------------
        # 2. BUSCAR OS PRODUTOS DISPONÍVEIS
        # ----------------------------------------------------
        # Recupera a lista de produtos fornecida pelo controller.
        produtos = pegar_produtos_venda()

        # Inicializa a variável que armazenará o produto
        # correspondente ao ID enviado pelo formulário.
        produto_encontrado = None

        # Percorre os produtos até encontrar o identificador
        # correspondente ao produto selecionado.
        for produto in produtos:

            # Converte os identificadores para string antes
            # da comparação, pois o formulário normalmente
            # envia o ID como texto.
            if str(produto["id"]) == str(produto_id):

                # Armazena os dados do produto encontrado.
                produto_encontrado = produto

                # Encerra a busca porque o produto já foi localizado.
                break

        # Se nenhum produto corresponder ao ID recebido,
        # interrompe o processamento e retorna à tela de vendas.
        if not produto_encontrado:
            return redirect(
                "/venda"
            )

        # ----------------------------------------------------
        # 3. CONSULTAR O ESTOQUE ATUAL
        # ----------------------------------------------------
        # Recupera os dados de estoque do produto selecionado.
        estoque = pegar_estoque_atual(
            produto_id
        )

        # A verificação de quantidade é executada quando
        # a consulta retorna um registro de estoque.
        #
        # Este comportamento é mantido conforme o código
        # original.
        if estoque:

            # Para vendas por caixa, a quantidade solicitada
            # precisa ser convertida em unidades individuais.
            if tipo_venda == "caixa":

                # Exemplo:
                # 2 caixas com 12 unidades cada = 24 unidades.
                quantidade_solicitada = (
                    quantidade
                    * produto_encontrado[
                        "quantidade_por_caixa"
                    ]
                )

            else:

                # Para os demais tipos de venda, conserva
                # a quantidade informada no formulário.
                quantidade_solicitada = quantidade

            # Compara a quantidade solicitada com o estoque
            # disponível em unidades.
            if (
                quantidade_solicitada
                > estoque["quantidade_atual_unidade"]
            ):

                # Informa que o estoque disponível não atende
                # à quantidade solicitada.
                flash(
                    "Estoque insuficiente para essa venda!",
                    "error"
                )

                # Interrompe a operação e retorna à tela.
                return redirect(
                    "/venda"
                )

        # ----------------------------------------------------
        # 4. DEFINIR O PREÇO UNITÁRIO
        # ----------------------------------------------------
        # O preço depende do tipo de venda selecionado.
        # As condições abaixo mantêm a lógica original
        # de preços do sistema.

        if tipo_venda == "dose":

            # Para venda por dose, utiliza o preço da dose.
            # Se o preço estiver vazio ou for None, utiliza zero.
            preco_unitario = float(
                produto_encontrado["preco_dose"] or 0
            )

        elif tipo_venda == "solto":

            # Para venda do produto solto, utiliza o preço
            # cadastrado especificamente para essa modalidade.
            preco_unitario = float(
                produto_encontrado["preco_unidade"] or 0
            )

        elif tipo_venda == "unidade":

            # Para venda por unidade, utiliza o preço de venda.
            preco_unitario = float(
                produto_encontrado["preco_venda"]
            )

        elif tipo_venda == "caixa":

            # Verifica se existe um preço específico para caixa.
            if produto_encontrado["preco_caixa"]:

                # Quando existe, utiliza o preço da caixa.
                preco_unitario = float(
                    produto_encontrado["preco_caixa"]
                )

            else:

                # Quando não existe um preço específico,
                # calcula o preço da caixa multiplicando
                # o preço unitário pela quantidade da caixa.
                preco_unitario = (
                    float(
                        produto_encontrado["preco_venda"]
                    )
                    * int(
                        produto_encontrado[
                            "quantidade_por_caixa"
                        ]
                    )
                )

        else:

            # Para qualquer outro tipo de venda, mantém
            # o preço de venda cadastrado para o produto.
            preco_unitario = float(
                produto_encontrado["preco_venda"]
            )

        # ----------------------------------------------------
        # 5. CALCULAR O SUBTOTAL
        # ----------------------------------------------------
        # O subtotal representa o preço unitário multiplicado
        # pela quantidade escolhida.
        subtotal = (
            preco_unitario
            * quantidade
        )

        # ----------------------------------------------------
        # 6. RECUPERAR OU INICIALIZAR O CARRINHO
        # ----------------------------------------------------
        # Se a chave 'carrinho' ainda não existir na sessão,
        # cria uma lista vazia para receber os itens.
        if "carrinho" not in session:
            session["carrinho"] = []

        # Obtém a lista atual do carrinho.
        carrinho = session["carrinho"]

        # ----------------------------------------------------
        # 7. VERIFICAR SE O PRODUTO JÁ ESTÁ NO CARRINHO
        # ----------------------------------------------------
        # Inicialmente, considera que ainda não existe
        # um item equivalente no carrinho.
        item_existente = None

        # Percorre os itens existentes para verificar se
        # algum corresponde ao mesmo produto e tipo de venda.
        for item in carrinho:

            # Os itens de sinuca não devem ser comparados
            # com produtos comuns.
            if item.get("tipo_item") == "sinuca":
                continue

            # Um item é considerado equivalente quando
            # possui o mesmo produto e o mesmo tipo de venda.
            if (
                item["produto_id"] == produto_id
                and item["tipo_venda"] == tipo_venda
            ):

                # Guarda a referência do item já existente.
                item_existente = item

                # Encerra a busca para evitar outro agrupamento.
                break

        # ----------------------------------------------------
        # 8. ATUALIZAR OU CRIAR O ITEM DO CARRINHO
        # ----------------------------------------------------
        if item_existente:

            # Se o produto já estiver no carrinho com o mesmo
            # tipo de venda, soma a nova quantidade à existente.
            item_existente["quantidade"] += quantidade

            # Atualiza o subtotal somando o valor da nova inclusão.
            item_existente["subtotal"] += subtotal

        else:

            # Se não houver item equivalente, adiciona um novo
            # dicionário à lista do carrinho.
            #
            # Cada chave armazena uma informação utilizada
            # para exibir ou calcular o item na interface.
            carrinho.append({
                # Identificador do produto no banco de dados.
                "produto_id": produto_id,

                # Nome utilizado na apresentação do carrinho.
                "nome": produto_encontrado["nome"],

                # Caminho ou referência da imagem do produto.
                "imagem": produto_encontrado["imagem"],

                # Modalidade da venda: dose, solto, unidade,
                # caixa ou outro valor permitido pelo sistema.
                "tipo_venda": tipo_venda,

                # Quantidade selecionada pelo usuário.
                "quantidade": quantidade,

                # Registra o preço utilizado na inclusão.
                "preco_original": preco_unitario,

                # Preço unitário aplicado ao item.
                "preco_unitario": preco_unitario,

                # Valor total correspondente à quantidade.
                "subtotal": subtotal
            })

        # ----------------------------------------------------
        # 9. SALVAR O CARRINHO NA SESSÃO
        # ----------------------------------------------------
        # Atualiza a chave da sessão com a lista modificada.
        session["carrinho"] = carrinho

        # Informa ao usuário que o produto foi adicionado.
        flash(
            f"{produto_encontrado['nome']} adicionado ao carrinho!",
            "success"
        )

        # Retorna à tela principal de vendas.
        return redirect(
            "/venda"
        )

    # --------------------------------------------------------
    # HISTÓRICO DE VENDAS
    # --------------------------------------------------------
    # URL: /venda/historico
    # Método: GET
    #
    # Exige autenticação e perfil de administrador ou gerente.
    # Busca os registros de vendas e apresenta o histórico.
    @app.route(
        "/venda/historico"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def historico_vendas():
        """
        Exibe o histórico de vendas do sistema.
        """

        # Recupera os registros do histórico pelo controller.
        vendas = pegar_historico_vendas()

        # Renderiza a página de histórico e envia os registros.
        return render_template(
            "venda/historico_vendas.html",
            vendas=vendas
        )

    # --------------------------------------------------------
    # DETALHES DE UMA VENDA
    # --------------------------------------------------------
    # URL: /venda/detalhes/<venda_id>
    # Método: GET
    #
    # Busca os produtos associados à venda e adiciona à lista
    # as fichas de sinuca registradas para o mesmo identificador.
    @app.route(
        "/venda/detalhes/<int:venda_id>"
    )
    def detalhes_venda(venda_id):
        """
        Exibe os produtos e as fichas de sinuca de uma venda.
        """

        # Recupera os produtos associados à venda.
        # A função retorna a estrutura esperada pelo template.
        produtos = pegar_detalhes_venda(
            venda_id
        )

        # Recupera as fichas de sinuca associadas à mesma venda.
        fichas = buscar_fichas_venda(
            venda_id
        )

        # Percorre as fichas para incluí-las na lista
        # que será apresentada na página de detalhes.
        for ficha in fichas:

            # Converte cada ficha em um dicionário com os campos
            # utilizados pelo template de detalhes.
            #
            # A ficha é identificada como um item de sinuca
            # e não como um produto comum do catálogo.
            produtos.append({
                "nome": "Ficha de Sinuca",
                "quantidade": ficha["quantidade_fichas"],
                "tipo_venda": "sinuca",
                "preco_unitario": ficha["valor_unitario"],
                "subtotal": ficha["valor_total"]
            })

        # Renderiza a página de detalhes com a lista combinada
        # de produtos e fichas de sinuca.
        return render_template(
            "venda/detalhes_venda.html",
            produtos=produtos
        )

    # --------------------------------------------------------
    # ADICIONAR FICHA DE SINUCA AO CARRINHO
    # --------------------------------------------------------
    # URL: /carrinho/adicionar-ficha
    # Método: POST
    #
    # Encaminha a operação ao controller de sinuca, que é
    # responsável por adicionar a ficha ao carrinho.
    @app.route(
        "/carrinho/adicionar-ficha",
        methods=["POST"]
    )
    def adicionar_ficha_route():
        """
        Solicita a inclusão de fichas de sinuca no carrinho.
        """

        # Executa a função responsável pela inclusão da ficha.
        adicionar_ficha_carrinho()

        # Exibe a mensagem de confirmação.
        flash(
            "Ficha de sinuca adicionada ao carrinho!",
            "success"
        )

        # Retorna à tela principal de vendas.
        return redirect(
            "/venda"
        )
