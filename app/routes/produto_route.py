# Importa funções do Flask
from flask import (
    render_template,
    request,
    redirect
)

# Importa controllers
from app.controllers.produto_controller import (
    pegar_produtos,
    cadastrar_produto_controller,
    pegar_produto_por_id,
    editar_produto_controller,
    inativar_produto_controller,
    ativar_produto_controller
)

from werkzeug.utils import secure_filename
import os

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

        nome = request.form.get(
        "nome"
    )

        categoria = request.form.get(
        "categoria"
    )

        sabor = request.form.get(
        "sabor"
    )

        tipo_embalagem = request.form.get(
        "tipo_embalagem"
    )

        volume = request.form.get(
        "volume"
    )

        preco_venda = request.form.get(
        "preco_venda"
    )

        quantidade_por_caixa = request.form.get(
        "quantidade_por_caixa"
    )

        vende_por_dose = (
        request.form.get(
            "vende_por_dose"
        ) is not None
    )

        volume_dose_ml = request.form.get(
        "volume_dose_ml"
    )
        
        imagem = request.files.get(
        "imagem"
    )
        
        nome_imagem = None

        if imagem and imagem.filename != "":

            nome_imagem = secure_filename(
        imagem.filename
    )

            caminho = os.path.join(
        "app/static/uploads/produtos",
        nome_imagem
    )

            imagem.save(caminho)

        cadastrar_produto_controller(

        nome,
        categoria,
        sabor,
        tipo_embalagem,
        volume,
        preco_venda,
        quantidade_por_caixa,
        vende_por_dose,
        volume_dose_ml,
        nome_imagem

    )

        return redirect(
        "/produto"
    )
    # ==========================
# ROTA: TELA EDITAR
# ==========================
    @app.route(
        "/produto/editar/<int:produto_id>"
    )
    def editar_produto(

        produto_id
    ):

        produto = pegar_produto_por_id(
            produto_id
        )

        return render_template(

            "produto/editar_produto.html",

            produto=produto
        )


    # ==========================
    # ROTA: SALVAR EDIÇÃO
    # ==========================
    @app.route(
        "/produto/atualizar/<int:produto_id>",
        methods=["POST"]
    )
    def atualizar_produto(

        produto_id
    ):

        nome = request.form.get("nome")

        categoria = request.form.get("categoria")

        sabor = request.form.get("sabor")

        tipo_embalagem = request.form.get(
    "tipo_embalagem"
)

        volume = request.form.get("volume")

        preco_venda = request.form.get(
    "preco_venda"
)

        quantidade_por_caixa = request.form.get(
    "quantidade_por_caixa"
)

        vende_por_dose = (
    request.form.get("vende_por_dose")
    == "on"
)

        volume_dose_ml = request.form.get(
    "volume_dose_ml"
)

        editar_produto_controller(

            produto_id,

    nome,

    categoria,

    sabor,

    tipo_embalagem,

    volume,

    preco_venda,

    quantidade_por_caixa,

    vende_por_dose,

    volume_dose_ml
        )

        return redirect(
            "/produto"
        )


    # ==========================
    # ROTA: INATIVAR PRODUTO
    # ==========================
    @app.route(
    "/produto/inativar/<int:produto_id>",
    methods=["POST"]
)
    def inativar_produto(produto_id):

        inativar_produto_controller(
        produto_id
    )

        return redirect("/produto")


    # ==========================
    # ROTA: ATIVAR PRODUTO
    # ==========================
    @app.route(
    "/produto/ativar/<int:produto_id>",
    methods=["POST"]
)
    def ativar_produto_route(produto_id):

        ativar_produto_controller(
        produto_id
    )

        return redirect("/produto")