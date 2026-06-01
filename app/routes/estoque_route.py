# Importa funções do Flask
from flask import (
    render_template,
    request,
    redirect
)

# Importa controller do estoque
from app.controllers.estoque_controller import (
    pegar_estoque,
    cadastrar_estoque_controller
)

# Importa controller produto
from app.controllers.produto_controller import (
    pegar_produtos,
    pegar_categorias
)

# Importa controller fornecedor
from app.controllers.fornecedor_controller import (
    pegar_fornecedores
)
# ==========================
# CONFIGURAR ROTAS ESTOQUE
# ==========================
def configurar_estoque_routes(app):

    # ==========================
    # ROTA: LISTAR ESTOQUE
    # ==========================
    @app.route("/estoque")
    def estoque():

        # Busca estoque
        dados_estoque = pegar_estoque()

        # Busca produtos
        produtos = pegar_produtos()

        # Busca categorias
        categorias = pegar_categorias()

        # Busca fornecedores
        fornecedores = pegar_fornecedores()

        # Envia dados para HTML
        return render_template(
            "estoque/estoque.html",

            estoque=dados_estoque,
            produtos=produtos,
            categorias=categorias,
            fornecedores=fornecedores
        )

    # ==========================
    # ROTA: CADASTRAR ESTOQUE
    # ==========================
    @app.route(
        "/estoque/cadastrar",
        methods=["POST"]
    )
    def cadastrar_estoque_route():

        # Produto
        produto_id = request.form.get(
            "produto_id"
        )

        # Origem compra
        origem_compra_id = request.form.get(
            "origem_compra_id"
        )

        # Nome do local
        nome_origem = request.form.get(
            "nome_origem"
        )

        # Fornecedor
        fornecedor_id = request.form.get(
            "fornecedor_id"
        )

        # Se vazio, vira None
        if fornecedor_id == "":

            fornecedor_id = None

        # Tipo entrada
        tipo_entrada = request.form.get(
            "tipo_entrada"
        )

        # Quantidade caixa
        quantidade_recebida_caixa = (
            request.form.get(
                "quantidade_recebida_caixa"
            )
        )

        # Quantidade unidade
        quantidade_recebida_unidade = (
            request.form.get(
                "quantidade_recebida_unidade"
            )
        )

        # Preço total
        preco_total_compra = request.form.get(
            "preco_total_compra"
        )

        # Data
        data_entrada = request.form.get(
            "data_entrada"
        )

        # Envia controller
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

        # Atualiza página
        return redirect("/estoque")