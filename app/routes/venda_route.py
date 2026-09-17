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
    pegar_historico_vendas,
    cadastrar_venda_controller,
    pegar_detalhes_venda
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

# Importa controller sinuca
from app.controllers.sinuca_controller import (
    pegar_config_sinuca,
    adicionar_ficha_carrinho,
    buscar_fichas_venda
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

        # Busca config de sinuca
        config_sinuca = pegar_config_sinuca()

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

        quantidade_fichas = 0

        for item in carrinho:

            if item.get("tipo_item") == "sinuca":

                quantidade_fichas = item["quantidade"]

                break

        # Envia HTML
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
        ).strip()


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

            print(produto_encontrado)

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
        "Estoque insuficiente para essa venda!",
        "danger"
    )

                return redirect(
        "/venda"
    )

       
        # ----------------------
        # PREÇO
        # ----------------------

        if tipo_venda == "dose":

            preco_unitario = float(
        produto_encontrado["preco_dose"] or 0
    )

        elif tipo_venda == "solto":

            preco_unitario = float(
        produto_encontrado["preco_unidade"] or 0
    )

        elif tipo_venda == "unidade":

            preco_unitario = float(
        produto_encontrado["preco_venda"]
    )

        elif tipo_venda == "caixa":

            if produto_encontrado["preco_caixa"]:

                preco_unitario = float(
            produto_encontrado["preco_caixa"]
        )

            else:

                preco_unitario = (
            float(produto_encontrado["preco_venda"])
            * int(produto_encontrado["quantidade_por_caixa"])
        )

        else:

            preco_unitario = float(
        produto_encontrado["preco_venda"]
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

            # Ignora ficha de sinuca
            if item.get("tipo_item") == "sinuca":

                continue

            if (

                item["produto_id"] == produto_id

                and

                item["tipo_venda"] == tipo_venda
    ):

                item_existente = item

                break

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
    
    # ==========================
    # HISTÓRICO DE VENDAS
    # ==========================
    @app.route("/venda/historico")
    def historico_vendas():

        vendas = pegar_historico_vendas()

        return render_template(

        "venda/historico_vendas.html",

        vendas=vendas
    )

    # ==========================
    # DETALHES DA VENDA
    # ==========================
    @app.route(
    "/venda/detalhes/<int:venda_id>"
)
    def detalhes_venda(venda_id):

        produtos = pegar_detalhes_venda(
        venda_id
    )

        fichas = buscar_fichas_venda(
        venda_id
    )

        for ficha in fichas:

            produtos.append({

            "nome": "Ficha de Sinuca",

            "quantidade":
                ficha["quantidade_fichas"],

            "tipo_venda":
                "sinuca",

            "preco_unitario":
                ficha["valor_unitario"],

            "subtotal":
                ficha["valor_total"]

        })

        return render_template(

        "venda/detalhes_venda.html",

        produtos=produtos
    )
    # ==========================
    # ADICIONAR FICHA AO CARRINHO
    # ==========================
    @app.route(
    "/carrinho/adicionar-ficha",
    methods=["POST"]
)
    def adicionar_ficha_route():

        adicionar_ficha_carrinho()

        return redirect(
        "/venda"
    )