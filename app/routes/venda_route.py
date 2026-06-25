# Importa Flask
from flask import (

    render_template,
    request,
    redirect,
    session
)

# Importa controller venda
from app.controllers.vendas_controller import (

    pegar_vendas,
    cadastrar_venda_controller
)

# Importa controller produto
from app.controllers.produto_controller import (

    pegar_produtos,
    pegar_categorias
)

# Importa controller cliente
from app.controllers.cliente_controller import (
    pegar_clientes
)

# Importa controller estoque
from app.controllers.estoque_controller import (
    baixar_estoque_controller
)

# Importa controller estoque
from app.controllers.estoque_controller import (
    pegar_estoque_atual
)



# ==========================
# CONFIGURAR ROTAS
# ==========================
def configurar_venda_routes(app):

    # ==========================
    # LISTAR VENDAS
    # ==========================
    @app.route("/venda")
    def venda():

        # Busca vendas
        vendas = pegar_vendas()

        # Busca produtos
        produtos = pegar_produtos()

        # Busca categorias
        categorias = pegar_categorias()

        # Busca clientes
        clientes = pegar_clientes()

        # Carrinho
        carrinho = session.get(
            "carrinho",
            []
        )

        # Total carrinho
        total_carrinho = 0

        for item in carrinho:

            total_carrinho += item[
                "subtotal"
            ]

        # Envia HTML
        return render_template(

        "venda/venda.html",

        vendas=vendas,

        produtos=produtos,

        categorias=categorias,

        clientes=clientes,

        carrinho=carrinho,

        total_carrinho=total_carrinho
)

    # ==========================
    # CADASTRAR VENDA
    # ==========================
    @app.route(
        "/venda/cadastrar",
        methods=["POST"]
    )
    def cadastrar_venda_route():

        # Produto
        produto_id = request.form.get(
            "produto_id"
        )

        # Quantidade
        quantidade = request.form.get(
            "quantidade"
        )

        # Tipo venda
        tipo_venda = request.form.get(
            "tipo_venda"
        )

        # Valor recebido
        valor_recebido = request.form.get(
            "valor_recebido"
        )

        # Status pagamento
        status_pagamento = request.form.get(
            "status_pagamento"
        )

        # Envia controller
        cadastrar_venda_controller(

            produto_id,

            quantidade,

            tipo_venda,

            valor_recebido,

            status_pagamento
        )

        # Atualiza página
        return redirect(
            "/venda"
        )

    # ==========================
    # ADICIONAR AO CARRINHO
    # ==========================
    @app.route(
        "/carrinho/adicionar",
        methods=["POST"]
    )
    def adicionar_carrinho():
        

        # Produto
        produto_id = request.form.get(
            "produto_id"
        )

        # Tipo venda
        tipo_venda = request.form.get(
            "tipo_venda"
        )

        # Quantidade
        quantidade = int(
            request.form.get(
                "quantidade"
            )
        )

        # Busca produtos
        produtos = pegar_produtos()

        # Procura produto
        produto_encontrado = None

        for produto in produtos:

            if str(produto["id"]) == str(produto_id):

                produto_encontrado = produto

                break

        # Se não encontrou
        if not produto_encontrado:

            return redirect("/venda")
    # ----------------------
    # VERIFICA ESTOQUE
    # ----------------------
        estoque = pegar_estoque_atual(

        produto_id
    )

        if estoque:

            if tipo_venda == "caixa":

                quantidade_solicitada = (

                    quantidade

                    * produto_encontrado[
                        "quantidade_por_caixa"
                    ]
                )

            else:

                quantidade_solicitada = (
                    quantidade
                )

            if (

                quantidade_solicitada

                >

                estoque[
                    "quantidade_atual_unidade"
                ]

            ):

                return redirect(
                    "/venda"
                )

       
        # ----------------------
        # PREÇO
        # ----------------------
        preco_unitario = float(
            produto_encontrado[
                "preco_venda"
            ]
        )

        # Caixa
        if tipo_venda == "caixa":

            preco_unitario *= int(
                produto_encontrado[
                    "quantidade_por_caixa"
                ]
            )

        # ----------------------
        # SUBTOTAL
        # ----------------------
        subtotal = (
            preco_unitario
            * quantidade
        )

        # ----------------------
        # CARRINHO
        # ----------------------
        if "carrinho" not in session:

            session["carrinho"] = []

        carrinho = session["carrinho"]

        # ----------------------
        # VERIFICA ITEM EXISTENTE
        # ----------------------
        item_existente = None

        for item in carrinho:

            if (

                item["produto_id"] == produto_id

                and

                item["tipo_venda"] == tipo_venda
            ):

                item_existente = item

                break

        # ----------------------
        # SOMA QUANTIDADE
        # ----------------------
        if item_existente:

            item_existente[
                "quantidade"
            ] += quantidade

            item_existente[
                "subtotal"
            ] += subtotal

        # ----------------------
        # NOVO ITEM
        # ----------------------
        else:

            carrinho.append({

                "produto_id": produto_id,

                "nome":
                produto_encontrado[
                    "nome"
                ],

                "tipo_venda":
                tipo_venda,

                "quantidade":
                quantidade,

                "preco_unitario":
                preco_unitario,

                "subtotal":
                subtotal
            })

        # Atualiza session
        session["carrinho"] = carrinho

        # Volta página
        return redirect("/venda")
    
    # ==========================
    # REMOVER DO CARRINHO
    # ==========================
    @app.route(
        "/carrinho/remover/<int:indice>",
        methods=["POST"]
    )
    def remover_carrinho(

        indice
    ):

        carrinho = session.get(
            "carrinho",
            []
        )

        if (

            indice >= 0

            and

            indice < len(carrinho)

        ):

            carrinho.pop(
                indice
            )

        session["carrinho"] = (
            carrinho
        )

        return redirect(
            "/venda"
        )

    # ==========================
    # FINALIZAR VENDA
    # ==========================
    @app.route(
        "/venda/finalizar",
        methods=["POST"]
    )
    def finalizar_venda():

        # Carrinho
        carrinho = session.get(
            "carrinho",
            []
        )

        # Se carrinho vazio
        if not carrinho:

            return redirect("/venda")

        # Tipo finalização
        tipo_finalizacao = request.form.get(
            "tipo_finalizacao"
       )

        # Cliente
        cliente_id = request.form.get(
            "cliente_id"
       )

        # Nome temporário
        nome_cliente_temporario = request.form.get(
            "nome_cliente_temporario"
        )
        
        # ----------------------
        # DEFINE PAGAMENTO
        # ----------------------

        status_pagamento = "Pago"

        conta_id = None

        # Venda fiado
        if tipo_finalizacao == "fiado":

            status_pagamento = "Pendente"

        # Conta pendente
        elif tipo_finalizacao == "pendente":

            status_pagamento = "Pendente"

        # Pagamento normal
        else:

            cliente_id = None

            nome_cliente_temporario = None

        # Valor recebido
        valor_recebido = request.form.get(
            "valor_recebido"
        )

        # Se vazio
        if not valor_recebido:

            valor_recebido = 0

        # ----------------------
        # TOTAL VENDA
        # ----------------------
        valor_total = 0

        for item in carrinho:

            valor_total += item[
                "subtotal"
            ]

        # ----------------------
        # TROCO
        # ----------------------
        troco = (
            float(valor_recebido)
            - valor_total
        )

        # ----------------------
        # IMPORTA CONEXÃO
        # ----------------------
        from app.database.conexao import conectar

        # Conecta banco
        conexao = conectar()

        # Cursor
        cursor = conexao.cursor()

        # ----------------------
        # SALDO DEVEDOR
        # ----------------------

        if tipo_finalizacao == "fiado":

            saldo_devedor = valor_total

        else:

            saldo_devedor = 0

        # ----------------------
        # INSERT VENDA
        # ----------------------
        sql_venda = """
            INSERT INTO venda (
            valor_total,
            valor_recebido,
            troco,
            cliente_id,
            status_pagamento,
            conta_id,
            nome_cliente_temporario,
            saldo_devedor
        )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Executa venda
        cursor.execute(

            sql_venda,

            (
                valor_total,
                valor_recebido,
                troco,
                cliente_id,
                status_pagamento,
                conta_id,
                nome_cliente_temporario,
                saldo_devedor
            )
        )

        # ID venda
        venda_id = cursor.lastrowid

        # ----------------------
        # PRODUTOS VENDA
        # ----------------------
        for item in carrinho:

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
                    %s, %s,
                    %s, %s,
                    %s, %s
                )
            """

            # Executa produto venda
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

            # ----------------------
            # BAIXA ESTOQUE
            # ----------------------
            baixar_estoque_controller(

                item["produto_id"],

                item["quantidade"],

                item["tipo_venda"]
            )

        # Salva banco
        conexao.commit()

        # Fecha cursor
        cursor.close()

        # Fecha conexão
        conexao.close()

        # ----------------------
        # LIMPA CARRINHO
        # ----------------------
        session["carrinho"] = []

        # Volta página
        return redirect("/venda")