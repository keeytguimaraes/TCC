# Importa Flask
from flask import (

    render_template,
    request,
    redirect,
    session,
    flash
)
from app.models.conta_model import (

                buscar_conta_aberta,
                criar_conta,
                atualizar_saldo_conta
            )


# Importa controller venda
from app.controllers.vendas_controller import (

    pegar_vendas,
    cadastrar_venda_controller
)

# Importa controller produto
from app.controllers.produto_controller import (

    pegar_produtos_venda,
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
        produtos = pegar_produtos_venda()

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
        produtos = pegar_produtos_venda()

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

                flash(
        "Estoque insuficiente para essa venda.",
        "danger"
    )

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

    "nome": produto_encontrado["nome"],

    "imagem": produto_encontrado["imagem"],

    "tipo_venda": tipo_venda,

    "quantidade": quantidade,

     "preco_original": preco_unitario,

    "preco_unitario": preco_unitario,

    "subtotal": subtotal
            })

        # Atualiza session
        session["carrinho"] = carrinho

        # Volta página
        return redirect("/venda")