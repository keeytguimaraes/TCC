
# ============================================================
# ROTAS DO CARRINHO — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis pelo funcionamento
# do carrinho de compras e pela finalização das vendas.
#
# Funcionalidades:
# - Exibir o carrinho;
# - Remover itens;
# - Limpar o carrinho;
# - Finalizar vendas pagas, fiados e contas pendentes;
# - Registrar fichas de sinuca;
# - Atualizar quantidades;
# - Alterar preços dos itens;
# - Consultar detalhes de uma conta pendente.
#
# A lista de produtos do carrinho é armazenada na sessão
# do Flask por meio de session["carrinho"].
#
# IMPORTANTE:
# As rotas recebem as requisições HTTP e coordenam as
# operações. Os controllers e models continuam responsáveis
# pelas operações que já realizam no sistema.
# ============================================================


# Decorator utilizado para exigir que o usuário esteja
# autenticado nas rotas em que ele já era utilizado.
from app.utils.auth import login_obrigatorio

# Ferramentas do Flask:
# - render_template: renderiza páginas HTML;
# - request: acessa os dados enviados pelo formulário;
# - redirect: redireciona para outra URL;
# - session: armazena dados associados à sessão;
# - flash: prepara mensagens temporárias para a interface.
from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

# Importa a função responsável por buscar os clientes.
from app.controllers.cliente_controller import (
    pegar_clientes
)

# Importa a função que realiza a baixa do estoque.
from app.controllers.estoque_controller import (
    baixar_estoque_controller
)

# Importa as funções que trabalham com contas de fiado
# e contas pendentes.
from app.models.conta_model import (
    buscar_conta_aberta,
    criar_conta,
    atualizar_saldo_conta,
    buscar_conta_pendente_aberta,
    criar_conta_pendente
)

# Importa a função que consulta o estoque atual de um produto.
from app.controllers.estoque_controller import (
    pegar_estoque_atual
)

# Importa a função que busca os dados de um produto.
from app.controllers.produto_controller import (
    pegar_produto_por_id
)

# Importa as funções utilizadas na consulta de contas.
from app.controllers.conta_controller import (
    pegar_contas,
    pegar_detalhes_conta
)

# Importa a conexão com o PostgreSQL.
# A importação fica no início do arquivo para centralizar
# as dependências utilizadas pelas rotas.
from app.database.conexao import conectar


# ============================================================
# CONFIGURAR ROTAS DO CARRINHO
# ============================================================
def configurar_carrinho_routes(app):
    """
    Registra as rotas do carrinho na aplicação Flask.

    Parâmetros:
        app: instância principal da aplicação Flask.

    Todas as funções de rota deste arquivo são registradas
    dentro desta função por meio dos decorators @app.route.
    """

    # --------------------------------------------------------
    # TELA DO CARRINHO
    # --------------------------------------------------------
    # URL: /carrinho
    # Método: GET
    #
    # Exibe os itens armazenados na sessão, a lista de clientes
    # e o total calculado a partir dos subtotais dos itens.
    @app.route("/carrinho")
    @login_obrigatorio
    def carrinho():
        """
        Carrega os dados necessários para exibir o carrinho.

        Se a sessão ainda não possuir um carrinho, utiliza uma
        lista vazia para evitar erros ao percorrer os itens.
        """

        # Recupera os itens da sessão.
        # Se a chave não existir, começa com uma lista vazia.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Busca os clientes que podem ser apresentados
        # no formulário de finalização da venda.
        clientes = pegar_clientes()

        # Inicializa o total antes de percorrer os itens.
        total_carrinho = 0

        # Soma o subtotal de cada item.
        # Cada item deve possuir a chave "subtotal".
        for item in carrinho:
            total_carrinho += item["subtotal"]

        # Envia os dados para o template responsável pela tela.
        return render_template(
            "carrinho/carrinho.html",
            carrinho=carrinho,
            clientes=clientes,
            total_carrinho=total_carrinho
        )

    # --------------------------------------------------------
    # REMOVER ITEM DO CARRINHO
    # --------------------------------------------------------
    # URL: /carrinho/remover/<indice>
    # Método: POST
    #
    # O índice identifica a posição do item na lista
    # armazenada na sessão.
    @app.route(
        "/carrinho/remover/<int:indice>",
        methods=["POST"]
    )
    def remover_carrinho(indice):
        """
        Remove um item do carrinho pelo índice recebido na URL.

        A verificação evita tentar remover uma posição que
        não exista na lista.
        """

        # Recupera o carrinho atual da sessão.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Verifica se o índice está dentro dos limites da lista.
        #
        # O índice precisa ser maior ou igual a zero e menor
        # que a quantidade total de itens.
        if (
            indice >= 0
            and indice < len(carrinho)
        ):
            # Remove o item localizado na posição indicada.
            carrinho.pop(indice)

        # Salva a lista atualizada na sessão, inclusive quando
        # o índice recebido não corresponde a um item válido.
        session["carrinho"] = carrinho

        # Retorna à tela do carrinho.
        return redirect("/carrinho")

    # --------------------------------------------------------
    # LIMPAR CARRINHO
    # --------------------------------------------------------
    # URL: /carrinho/limpar
    # Método: POST
    #
    # Substitui a lista atual por uma lista vazia.
    @app.route(
        "/carrinho/limpar",
        methods=["POST"]
    )
    def limpar_carrinho():
        """
        Remove todos os itens armazenados no carrinho da sessão.
        """

        # Salva uma lista vazia na sessão.
        session["carrinho"] = []

        # Retorna à tela do carrinho.
        return redirect("/carrinho")

    # --------------------------------------------------------
    # FINALIZAR VENDA
    # --------------------------------------------------------
    # URL: /carrinho/finalizar
    # Método: POST
    #
    # Esta rota registra a venda, os itens vendidos e,
    # quando aplicável, as informações de fiado, conta
    # pendente e fichas de sinuca.
    @app.route(
        "/carrinho/finalizar",
        methods=["POST"]
    )
    def finalizar_venda():
        """
        Processa a finalização do carrinho.

        O tipo de finalização é obtido do formulário por meio
        de "tipo_finalizacao".

        Os valores utilizados pelo fluxo original são:
            - "fiado";
            - "pendente";
            - "pago" para o pagamento normal.

        A rota mantém a sequência original das operações.
        """

        # ----------------------------------------------------
        # 1. RECUPERAR O CARRINHO
        # ----------------------------------------------------
        carrinho = session.get(
            "carrinho",
            []
        )

        # Não há venda a registrar quando o carrinho está vazio.
        # Nesse caso, retorna à tela sem continuar o processamento.
        if not carrinho:
            return redirect("/carrinho")

        # ----------------------------------------------------
        # 2. LER OS DADOS DO FORMULÁRIO
        # ----------------------------------------------------

        # Identifica o tipo de finalização selecionado na tela.
        tipo_finalizacao = request.form.get(
            "tipo_finalizacao"
        )

        # Obtém o ID do cliente, quando informado.
        cliente_id = request.form.get(
            "cliente_id"
        )

        # Obtém o nome temporário usado na conta pendente.
        nome_cliente_temporario = request.form.get(
            "nome_cliente_temporario"
        )

        # ----------------------------------------------------
        # 3. DEFINIR O STATUS E AS CONTAS RELACIONADAS
        # ----------------------------------------------------

        # O comportamento original começa considerando a venda
        # paga. Os fluxos de fiado e pendente alteram esse status.
        status_pagamento = "pago"

        # Inicializa os IDs como None porque a venda pode não
        # estar vinculada a uma conta de fiado ou pendente.
        conta_id = None
        conta_pendente_id = None

        # ----------------------------------------------------
        # VENDA NO FIADO
        # ----------------------------------------------------
        if tipo_finalizacao == "fiado":

            # Marca a venda como pendente de pagamento.
            status_pagamento = "pendente"

            # Procura uma conta de fiado aberta para o cliente.
            conta = buscar_conta_aberta(
                cliente_id
            )

            if conta:
                # Se já existir uma conta aberta, reutiliza seu ID.
                conta_id = conta["id"]

            else:
                # Se não existir, cria uma conta para o cliente.
                conta_id = criar_conta(
                    cliente_id
                )

        # ----------------------------------------------------
        # CONTA PENDENTE
        # ----------------------------------------------------
        elif tipo_finalizacao == "pendente":

            # A conta pendente também gera uma venda com
            # status de pagamento pendente.
            status_pagamento = "pendente"

            # Procura uma conta pendente aberta com o nome
            # temporário informado no formulário.
            conta_pendente = buscar_conta_pendente_aberta(
                nome_cliente_temporario
            )

            if conta_pendente:
                # Reutiliza a conta pendente já existente.
                conta_pendente_id = conta_pendente["id"]

            else:
                # Cria uma nova conta pendente se não houver
                # uma conta aberta com esse nome.
                conta_pendente_id = criar_conta_pendente(
                    nome_cliente_temporario
                )

        # ----------------------------------------------------
        # PAGAMENTO NORMAL
        # ----------------------------------------------------
        else:

            # No fluxo normal, a venda não fica vinculada
            # a um cliente nem a um nome temporário.
            cliente_id = None
            nome_cliente_temporario = None

        # ----------------------------------------------------
        # 4. OBTER O VALOR RECEBIDO
        # ----------------------------------------------------

        # Lê o valor recebido informado no formulário.
        valor_recebido = request.form.get(
            "valor_recebido"
        )

        # Preserva o comportamento original: se o formulário
        # não fornecer um valor, utiliza zero.
        if not valor_recebido:
            valor_recebido = 0

        # ----------------------------------------------------
        # 5. CALCULAR O TOTAL DO CARRINHO
        # ----------------------------------------------------

        # Começa com zero para somar os subtotais dos itens.
        valor_total = 0

        # Soma o subtotal de cada item do carrinho.
        for item in carrinho:
            valor_total += item["subtotal"]

        # ----------------------------------------------------
        # 6. CALCULAR O TROCO
        # ----------------------------------------------------

        # Converte o valor recebido para número e subtrai
        # o total da venda para obter o troco.
        troco = (
            float(valor_recebido)
            - valor_total
        )

        # ----------------------------------------------------
        # 7. ABRIR A CONEXÃO PARA REGISTRAR A VENDA
        # ----------------------------------------------------

        # Cria uma conexão e um cursor para executar os INSERTs
        # e UPDATEs relacionados à finalização.
        conexao = conectar()
        cursor = conexao.cursor()

        # ----------------------------------------------------
        # 8. DEFINIR O SALDO DEVEDOR
        # ----------------------------------------------------

        # No comportamento original, fiado e conta pendente
        # começam com o valor total da venda como saldo devedor.
        #
        # Uma venda normal começa com saldo devedor zero.
        if tipo_finalizacao in [
            "fiado",
            "pendente"
        ]:
            saldo_devedor = valor_total

        else:
            saldo_devedor = 0

        # ----------------------------------------------------
        # 9. REGISTRAR A VENDA PRINCIPAL
        # ----------------------------------------------------

        # Obtém o ID do usuário autenticado na sessão.
        # A rota depende de esse valor existir na sessão.
        usuario_id = session["usuario_id"]

        # Insere o registro principal na tabela venda.
        #
        # RETURNING id devolve o ID gerado pelo PostgreSQL,
        # necessário para relacionar os produtos e as fichas
        # de sinuca à venda recém-criada.
        sql_venda = """
            INSERT INTO venda (
                valor_total,
                valor_recebido,
                troco,
                cliente_id,
                status_pagamento,
                conta_id,
                conta_pendente_id,
                saldo_devedor,
                usuario_id
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id
        """

        cursor.execute(
            sql_venda,
            (
                valor_total,
                valor_recebido,
                troco,
                cliente_id,
                status_pagamento,
                conta_id,
                conta_pendente_id,
                saldo_devedor,
                usuario_id
            )
        )

        # Recupera o ID da venda inserida.
        # Este cursor é comum, não RealDictCursor, por isso
        # o resultado é acessado pela posição zero.
        venda_id = cursor.fetchone()[0]

        # Mantive a consulta e o print de depuração presentes
        # no código original, para não remover esse efeito.
        cursor.execute(
            "SELECT id FROM venda WHERE id = %s",
            (venda_id,)
        )

        print(
            "VENDA ENCONTRADA:",
            cursor.fetchone()
        )

        # ----------------------------------------------------
        # 10. ATUALIZAR O SALDO DA CONTA DE FIADO
        # ----------------------------------------------------

        # A atualização de saldo é executada apenas para o fiado.
        # A conta pendente segue o fluxo original separado.
        if tipo_finalizacao == "fiado":

            atualizar_saldo_conta(
                cursor,
                conta_id,
                valor_total
            )


        # ----------------------------------------------------
        # 11. REGISTRAR OS ITENS DO CARRINHO
        # ----------------------------------------------------
        # Percorre cada item para identificar se ele representa
        # uma ficha de sinuca ou um produto comercial normal.
        for item in carrinho:

            # ================================================
            # FICHA DE SINUCA
            # ================================================
            # Os itens de sinuca são identificados pela chave
            # "tipo_item" com o valor "sinuca".
            #
            # Eles são registrados em sinuca_venda, e não em
            # produto_venda, conforme o funcionamento original.
            if item.get("tipo_item") == "sinuca":

                sql_sinuca = """
                    INSERT INTO sinuca_venda (
                        venda_id,
                        cliente_id,
                        quantidade_fichas,
                        valor_unitario,
                        valor_total,
                        status_pagamento
                    )
                    VALUES (
                        %s, %s, %s,
                        %s, %s, %s
                    )
                """

                cursor.execute(
                    sql_sinuca,
                    (
                        venda_id,
                        cliente_id,
                        item["quantidade"],
                        item["preco_unitario"],
                        item["subtotal"],
                        status_pagamento
                    )
                )

                # O continue encerra o processamento deste item
                # e passa para o próximo elemento do carrinho.
                #
                # Isso impede que uma ficha de sinuca também
                # seja registrada como produto normal e evita
                # que este item passe pela baixa de estoque
                # de produtos comuns.
                continue

            # ================================================
            # PRODUTO COMERCIAL NORMAL
            # ================================================
            # Se o item não for de sinuca, registra o produto
            # na tabela que relaciona vendas e produtos.
            sql_produto_venda = """
                INSERT INTO produto_venda (
                    venda_id,
                    produto_id,
                    quantidade,
                    tipo_venda,
                    preco_unitario,
                    subtotal
                )
                VALUES (
                    %s, %s, %s,
                    %s, %s, %s
                )
            """

            cursor.execute(
                sql_produto_venda,
                (
                    venda_id,
                    item["produto_id"],
                    item["quantidade"],
                    item["tipo_venda"],
                    item["preco_unitario"],
                    item["subtotal"]
                )
            )

            # -----------------------------------------------
            # BAIXA DO ESTOQUE
            # -----------------------------------------------
            # Solicita ao controller a baixa do estoque
            # correspondente ao produto vendido.
            #
            # O controller recebe o ID do produto, a quantidade
            # e o tipo de venda para aplicar a lógica que já
            # está implementada nessa camada do sistema.
            baixar_estoque_controller(
                item["produto_id"],
                item["quantidade"],
                item["tipo_venda"]
            )

        # ----------------------------------------------------
        # 12. CONFIRMAR AS ALTERAÇÕES
        # ----------------------------------------------------
        # Confirma as operações executadas pela conexão aberta
        # nesta rota, incluindo o registro principal da venda,
        # os itens e as fichas de sinuca, além da atualização
        # de saldo realizada com o cursor recebido.
        conexao.commit()

        # Fecha o cursor e a conexão utilizados pela rota.
        cursor.close()
        conexao.close()

        # ----------------------------------------------------
        # 13. EXIBIR MENSAGEM DE RESULTADO
        # ----------------------------------------------------
        # A mensagem depende do tipo de finalização escolhido.
        # As categorias e os textos originais são preservados.
        if tipo_finalizacao == "pago":

            flash(
                "Venda concluída com sucesso!",
                "success"
            )

        elif tipo_finalizacao == "fiado":

            flash(
                "Venda registrada no fiado com sucesso!",
                "success"
            )

        elif tipo_finalizacao == "pendente":

            flash(
                "Conta registrada com sucesso!",
                "success"
            )

        # ----------------------------------------------------
        # 14. LIMPAR O CARRINHO
        # ----------------------------------------------------
        # Após a finalização, substitui o carrinho da sessão
        # por uma lista vazia para preparar uma nova venda.
        session["carrinho"] = []

        # Retorna à tela do carrinho.
        return redirect("/carrinho")


    # ========================================================
    # AUMENTAR QUANTIDADE
    # ========================================================
    # URL: /carrinho/mais/<indice>
    # Método: POST
    #
    # Aumenta a quantidade do item indicado.
    # Para produtos comuns, verifica o estoque antes de
    # atualizar a quantidade. Para sinuca, apenas recalcula
    # o subtotal, conforme a regra original.
    @app.route(
        "/carrinho/mais/<int:indice>",
        methods=["POST"]
    )
    def aumentar_quantidade(indice):

        # Recupera o carrinho atual.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Só acessa o item quando o índice é válido.
        if 0 <= indice < len(carrinho):

            # Recupera o item que terá a quantidade aumentada.
            item = carrinho[indice]

            # -----------------------------------------------
            # FICHA DE SINUCA
            # -----------------------------------------------
            if item.get("tipo_item") == "sinuca":

                # Acrescenta uma ficha à quantidade atual.
                item["quantidade"] += 1

                # Recalcula o subtotal multiplicando a nova
                # quantidade pelo preço unitário da ficha.
                item["subtotal"] = (
                    item["quantidade"]
                    * item["preco_unitario"]
                )

                # Salva o carrinho atualizado na sessão.
                session["carrinho"] = carrinho

                # Retorna imediatamente para a tela.
                # Não executa a verificação de estoque normal.
                return redirect("/carrinho")

            # -----------------------------------------------
            # PRODUTO COMERCIAL NORMAL
            # -----------------------------------------------

            # Busca os dados do produto para consultar, entre
            # outras informações, a quantidade por caixa.
            produto = pegar_produto_por_id(
                item["produto_id"]
            )

            # Consulta o estoque atual do produto.
            estoque = pegar_estoque_atual(
                item["produto_id"]
            )

            # Calcula a quantidade que o item terá após o
            # acréscimo de uma unidade comercializada.
            nova_quantidade = (
                item["quantidade"] + 1
            )

            # -----------------------------------------------
            # CONVERTER A QUANTIDADE PARA UNIDADES
            # -----------------------------------------------
            # Para uma venda por caixa, multiplica a quantidade
            # de caixas pela quantidade de unidades por caixa.
            if item["tipo_venda"] == "caixa":

                quantidade_solicitada = (
                    nova_quantidade
                    * produto["quantidade_por_caixa"]
                )

            else:

                # Nos demais tipos, preserva o cálculo original:
                # utiliza diretamente a nova quantidade.
                quantidade_solicitada = nova_quantidade

            # -----------------------------------------------
            # VERIFICAR ESTOQUE DISPONÍVEL
            # -----------------------------------------------
            # A quantidade solicitada só é aceita quando não
            # ultrapassa a quantidade atual de unidades.
            if (
                quantidade_solicitada
                <= estoque["quantidade_atual_unidade"]
            ):

                # Atualiza a quantidade do item no carrinho.
                item["quantidade"] = nova_quantidade

                # Acrescenta um preço unitário ao subtotal atual.
                # Mantém a forma de cálculo do código original.
                item["subtotal"] += item["preco_unitario"]

                # Persiste as alterações na sessão.
                session["carrinho"] = carrinho

        # Se o índice for inválido ou não houver estoque
        # suficiente, retorna à tela sem aplicar o aumento.
        return redirect("/carrinho")

    # ========================================================
    # DIMINUIR QUANTIDADE
    # ========================================================
    # URL: /carrinho/menos/<indice>
    # Método: POST
    #
    # Diminui a quantidade do item.
    # Quando o item possui apenas uma unidade, ele é removido.
    @app.route(
        "/carrinho/menos/<int:indice>",
        methods=["POST"]
    )
    def diminuir_quantidade(indice):

        # Recupera os itens armazenados na sessão.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Verifica se o índice recebido corresponde a um item.
        if 0 <= indice < len(carrinho):

            # Se a quantidade for maior que um, reduz uma unidade.
            if carrinho[indice]["quantidade"] > 1:

                carrinho[indice]["quantidade"] -= 1

                # Subtrai um preço unitário do subtotal.
                carrinho[indice]["subtotal"] -= (
                    carrinho[indice]["preco_unitario"]
                )

            else:

                # Se restar apenas uma unidade, remove o item
                # completamente do carrinho.
                carrinho.pop(indice)

            # Salva a lista atualizada na sessão.
            session["carrinho"] = carrinho

        # Retorna à tela do carrinho.
        return redirect("/carrinho")

    # ========================================================
    # ATUALIZAR QUANTIDADE
    # ========================================================
    # URL: /carrinho/atualizar/<indice>
    # Método: POST
    #
    # Recebe uma quantidade pelo formulário e recalcula
    # o subtotal com base no preço unitário já armazenado.
    @app.route(
        "/carrinho/atualizar/<int:indice>",
        methods=["POST"]
    )
    def atualizar_quantidade(indice):

        # Recupera o carrinho da sessão.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Só atualiza o item se o índice for válido.
        if 0 <= indice < len(carrinho):

            # Lê a quantidade enviada pelo formulário e
            # converte o valor recebido para um número inteiro.
            quantidade = int(
                request.form.get("quantidade")
            )

            # Impede que a quantidade seja menor que um.
            if quantidade < 1:
                quantidade = 1

            # Salva a nova quantidade no item selecionado.
            carrinho[indice]["quantidade"] = quantidade

            # Recalcula o subtotal em vez de somar ou subtrair
            # diferenças do valor anterior.
            carrinho[indice]["subtotal"] = (
                quantidade
                * carrinho[indice]["preco_unitario"]
            )

            # Atualiza a sessão com o carrinho modificado.
            session["carrinho"] = carrinho

        # Retorna à tela do carrinho.
        return redirect("/carrinho")

    # ========================================================
    # ALTERAR PREÇO UNITÁRIO
    # ========================================================
    # URL: /carrinho/preco/<indice>
    # Método: POST
    #
    # Altera o preço unitário de um item e recalcula
    # seu subtotal com a quantidade atual.
    @app.route(
        "/carrinho/preco/<int:indice>",
        methods=["POST"]
    )
    def alterar_preco(indice):

        # Recupera os itens do carrinho.
        carrinho = session.get(
            "carrinho",
            []
        )

        # Confere se o índice existe na lista.
        if 0 <= indice < len(carrinho):

            # Obtém o novo preço enviado pelo formulário.
            novo_preco = float(
                request.form.get("preco_unitario")
            )

            # Preserva a regra original: preços iguais ou
            # inferiores a zero não são aceitos.
            if novo_preco <= 0:
                return redirect("/carrinho")

            # Atualiza o preço unitário do item.
            carrinho[indice]["preco_unitario"] = novo_preco

            # Recalcula o subtotal usando a quantidade atual.
            carrinho[indice]["subtotal"] = (
                novo_preco
                * carrinho[indice]["quantidade"]
            )

            # Persiste a alteração na sessão.
            session["carrinho"] = carrinho

        # Retorna à tela do carrinho.
        return redirect("/carrinho")

    # ========================================================
    # DETALHES DA CONTA PENDENTE
    # ========================================================
    # URL: /conta/conta_pendente_detalhes/<conta_id>
    #
    # Busca os detalhes da conta pelo controller e envia
    # os dados ao template correspondente.
    @app.route(
        "/conta/conta_pendente_detalhes/<int:conta_id>"
    )
    def detalhes_conta(conta_id):

        # Solicita ao controller os dados da conta pendente.
        conta = pegar_detalhes_conta(
            conta_id
        )

        # Renderiza a página de detalhes com os dados recebidos.
        return render_template(
            "conta/conta_pendente_detalhes.html",
            conta=conta
        )
