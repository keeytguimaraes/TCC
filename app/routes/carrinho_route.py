# Importa Flask
from flask import (

    render_template,
    request,
    redirect,
    session
)

# Importa controller cliente
from app.controllers.cliente_controller import (
    pegar_clientes
)

# Importa controller estoque
from app.controllers.estoque_controller import (
    baixar_estoque_controller
)

# Importa model conta
from app.models.conta_model import (

    buscar_conta_aberta,
    criar_conta,
    atualizar_saldo_conta,

    buscar_conta_pendente_aberta,
    criar_conta_pendente
)


from app.controllers.estoque_controller import (
    pegar_estoque_atual
)

from app.controllers.produto_controller import (
    pegar_produto_por_id
)

from app.controllers.conta_controller import (
    pegar_contas,
    pegar_detalhes_conta
)

# ==========================
# CONFIGURAR ROTAS
# ==========================
def configurar_carrinho_routes(app):


    # ==========================
    # TELA CARRINHO
    # ==========================
    @app.route("/carrinho")
    def carrinho():

        carrinho = session.get(
            "carrinho",
            []
        )

        clientes = pegar_clientes()

        total_carrinho = 0

        for item in carrinho:

            total_carrinho += item[
                "subtotal"
            ]

        return render_template(

            "carrinho/carrinho.html",

            carrinho=carrinho,

            clientes=clientes,

            total_carrinho=total_carrinho
        )


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
            "/carrinho"
        )
    
    # ==========================
    # LIMPAR CARRINHO
    # ==========================
    @app.route(
    "/carrinho/limpar",
    methods=["POST"]
)
    def limpar_carrinho():

        session["carrinho"] = []

        return redirect(
        "/carrinho"
    )


    # ==========================
    # FINALIZAR VENDA
    # ==========================
    @app.route(
        "/carrinho/finalizar",
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

            return redirect(
                "/carrinho"
            )

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

        conta_pendente_id = None

        # Venda fiado
        if tipo_finalizacao == "fiado":

            status_pagamento = "Pendente"

            conta = buscar_conta_aberta(
                cliente_id
            )

            if conta:

                conta_id = conta["id"]

            else:

                conta_id = criar_conta(
                    cliente_id
                )

        # Conta pendente
        elif tipo_finalizacao == "pendente":

            status_pagamento = "Pendente"

            conta_pendente = (
        buscar_conta_pendente_aberta(
            nome_cliente_temporario
        )
    )

            if conta_pendente:

                conta_pendente_id = (
            conta_pendente["id"]
        )

            else:

                conta_pendente_id = (
            criar_conta_pendente(
                nome_cliente_temporario
            )
        )

        # Pagamento normal
        else:

            cliente_id = None

            nome_cliente_temporario = None

        # ----------------------
        # VALOR RECEBIDO
        # ----------------------
        valor_recebido = request.form.get(
            "valor_recebido"
        )

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
        # CONEXÃO
        # ----------------------
        from app.database.conexao import conectar

        conexao = conectar()

        cursor = conexao.cursor()

        # ----------------------
        # SALDO DEVEDOR
        # ----------------------
        if tipo_finalizacao in [

            "fiado",

            "pendente"

        ]:

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
                conta_pendente_id,
                saldo_devedor

            )
            VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s
            )
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
                saldo_devedor
            )
        )

        venda_id = cursor.lastrowid

        cursor.execute(
    "SELECT id FROM venda WHERE id = %s",
    (venda_id,)
)

        print(
    "VENDA ENCONTRADA:",
    cursor.fetchone()
)


        # ----------------------
        # ATUALIZA CONTA
        # ----------------------
        if tipo_finalizacao == "fiado":

            atualizar_saldo_conta(

                cursor,

                conta_id,

                valor_total
            )

        # ----------------------
        # PRODUTOS DA VENDA
        # ----------------------
        for item in carrinho:

        # ======================
        # FICHA DE SINUCA
        # ======================
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

    %s,
    %s,
    %s,
    %s,
    %s,
    %s
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

               continue

    # ======================
    # PRODUTOS NORMAIS
    # ======================
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
        conexao.commit()

        cursor.close()

        conexao.close()

        # ----------------------
        # LIMPA CARRINHO
        # ----------------------
        session["carrinho"] = []

        return redirect(
            "/carrinho"
        )
    
    # ==========================
    # AUMENTAR QUANTIDADE
    # ==========================
    @app.route(
    "/carrinho/mais/<int:indice>",
    methods=["POST"]
)
    def aumentar_quantidade(indice):

        carrinho = session.get(
        "carrinho",
        []
    )

        if 0 <= indice < len(carrinho):

            item = carrinho[indice]

        item = carrinho[indice]

        # ----------------------
        # FICHA DE SINUCA
        # ----------------------
        if item.get("tipo_item") == "sinuca":

            item["quantidade"] += 1

            item["subtotal"] = (
        item["quantidade"]
        * item["preco_unitario"]
    )

            session["carrinho"] = carrinho

            return redirect(
        "/carrinho"
    )

        # ----------------------
        # PRODUTO NORMAL
        # ----------------------
        produto = pegar_produto_por_id(
    item["produto_id"]
)

        estoque = pegar_estoque_atual(
    item["produto_id"]
)

        nova_quantidade = (
    item["quantidade"] + 1
)

            # ----------------------
            # CONVERTE PARA UNIDADES
            # ----------------------
        if item["tipo_venda"] == "caixa":

                quantidade_solicitada = (

                nova_quantidade

                * produto[
                    "quantidade_por_caixa"
                ]
            )

        else:

                quantidade_solicitada = (
                nova_quantidade
            )

            # ----------------------
            # VERIFICA ESTOQUE
            # ----------------------
        if (

            quantidade_solicitada

            <=

                estoque[
                "quantidade_atual_unidade"
            ]

        ):

                item["quantidade"] = (
                nova_quantidade
            )

                item["subtotal"] += (
                item["preco_unitario"]
            )

                session["carrinho"] = (
                carrinho
            )

        return redirect(
        "/carrinho"
    )


    # ==========================
    # DIMINUIR QUANTIDADE
    # ==========================
    @app.route(
    "/carrinho/menos/<int:indice>",
    methods=["POST"]
)
    def diminuir_quantidade(indice):

        carrinho = session.get(
        "carrinho",
        []
    )

        if 0 <= indice < len(carrinho):

            if carrinho[indice][
            "quantidade"
        ] > 1:

                carrinho[indice][
                "quantidade"
            ] -= 1

                carrinho[indice][
                "subtotal"
            ] -= carrinho[indice][
                "preco_unitario"
            ]

            else:

                carrinho.pop(
                indice
            )

            session["carrinho"] = (
            carrinho
        )

        return redirect(
        "/carrinho"
    )


    # ==========================
    # ATUALIZAR QUANTIDADE
    # ==========================
    @app.route(
    "/carrinho/atualizar/<int:indice>",
    methods=["POST"]
)
    def atualizar_quantidade(indice):

        carrinho = session.get(
        "carrinho",
        []
    )

        if 0 <= indice < len(carrinho):

            quantidade = int(
            request.form.get(
                "quantidade"
            )
        )

            if quantidade < 1:

                quantidade = 1

            carrinho[indice][
            "quantidade"
        ] = quantidade

            carrinho[indice][
            "subtotal"
        ] = (

                quantidade

            *

                carrinho[indice][
                "preco_unitario"
            ]
        )

            session["carrinho"] = carrinho

        return redirect(
        "/carrinho"
    )

    # ==========================
    # ALTERAR PREÇO
    # ==========================
    @app.route(
    "/carrinho/preco/<int:indice>",
    methods=["POST"]
)
    def alterar_preco(indice):

        carrinho = session.get(
        "carrinho",
        []
    )

        if 0 <= indice < len(carrinho):

            novo_preco = float(
                request.form.get(
        "preco_unitario"
    )
)

            if novo_preco <= 0:

                return redirect(
        "/carrinho"
    )

            carrinho[indice][
            "preco_unitario"
        ] = novo_preco

            carrinho[indice][
            "subtotal"
        ] = (

                novo_preco

            *

                carrinho[indice][
                "quantidade"
            ]
        )

            session["carrinho"] = (
            carrinho
        )

        return redirect(
        "/carrinho"
    )

    # ==========================
    # DETALHES
    # ==========================
    @app.route(
    "/conta/conta_pendente_detalhes/<int:conta_id>"
)
    def detalhes_conta(conta_id):

        conta = pegar_detalhes_conta(
        conta_id
    )

        return render_template(

        "conta/conta_pendente_detalhes.html",

        conta=conta
    )