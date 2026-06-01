# Importa funções do Flask
from flask import (
    render_template,
    request,
    redirect
)

# Importa controllers
from app.controllers.produto_controller import (
    pegar_produtos,
    cadastrar_produto_controller
)


# Função responsável
# por registrar rotas
def configurar_produto_routes(app):

    # ==========================
    # ROTA: LISTAR PRODUTOS
    # ==========================
    @app.route("/produto")
    def produto():

        # Busca produtos
        dados = pegar_produtos()

        # Envia para HTML
        return render_template(
            "produto/produto.html",

            # Variável do HTML
            produtos=dados
        )


    # ==========================
    # ROTA: CADASTRAR PRODUTO
    # ==========================
    @app.route(
        "/produto/cadastrar",
        methods=["POST"]
    )
    def cadastrar_produto():

        # Pega dados do formulário
        nome = request.form.get(
            "nome"
        )

        categoria = request.form.get(
            "categoria"
        )

        preco_venda = request.form.get(
            "preco_venda"
        )

        quantidade_por_caixa = request.form.get(
            "quantidade_por_caixa"
        )

        # Envia para controller
        cadastrar_produto_controller(
            nome,
            categoria,
            preco_venda,
            quantidade_por_caixa
        )

        # Atualiza tela
        return redirect("/produto")