# Importa funções do Flask
from flask import (
    render_template,
    request,
    redirect
)

# Importa controllers
from app.controllers.produto_controller import (
    pegar_produtos,
    pegar_produtos_ativos,
    pegar_produtos_inativos,
    cadastrar_produto_controller,
    pegar_produto_por_id,
    editar_produto_controller,
    inativar_produto_controller,
    ativar_produto_controller,
    pegar_historico_preco
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
    
    @app.route("/produto/ativos")
    def produtos_ativos():

        dados = pegar_produtos_ativos()

        return render_template(
        "produto/produto.html",
        produtos=dados
    )

    @app.route("/produto/inativos")
    def produtos_inativos():

        dados = pegar_produtos_inativos()

        return render_template(
        "produto/produto.html",
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

    # --------------------------
    # DADOS BÁSICOS
    # --------------------------
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

    # --------------------------
    # VOLUME / PESO
    # --------------------------
      valor_volume = float(
        request.form.get(
            "valor_volume",
            0
        )
    )

      unidade_volume = request.form.get(
        "unidade_volume"
    )
      

    # Texto exibido no sistema
      volume = (
        str(valor_volume)
        + unidade_volume
    )

     # Valor convertido para base
      if unidade_volume == "L":

          quantidade_por_unidade = (
            valor_volume * 1000
        )

      elif unidade_volume == "kg":

          quantidade_por_unidade = (
            valor_volume * 1000
        )

      else:

          quantidade_por_unidade = (
            valor_volume
        )

    # --------------------------
    # PREÇOS
    # --------------------------
      preco_venda = request.form.get(
        "preco_venda"
    )

      preco_dose = request.form.get(
        "preco_dose"
    )

      preco_unidade = request.form.get(
        "preco_unidade"
    )

    # --------------------------
    # ESTOQUE
    # --------------------------
      quantidade_por_caixa = request.form.get(
        "quantidade_por_caixa"
    )

      estoque_minimo = request.form.get(
        "estoque_minimo"
    )

    # --------------------------
    # TIPOS DE VENDA
    # --------------------------
      vende_por_dose = (
        request.form.get(
            "vende_por_dose"
        ) is not None
    )

      vende_por_unidade = (
        request.form.get(
            "vende_por_unidade"
        ) is not None
    )

      volume_dose_ml = request.form.get(
        "volume_dose_ml"
    )

    # --------------------------
    # IMAGEM
    # --------------------------
    
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

          imagem.save(
            caminho
        )

    # --------------------------
    # SALVA PRODUTO
    # --------------------------
      cadastrar_produto_controller(

        nome,
        categoria,
        sabor,
        tipo_embalagem,
        volume,
        preco_venda,
        quantidade_por_caixa,
        estoque_minimo,
        vende_por_dose,
        vende_por_unidade,
        volume_dose_ml,
        preco_dose,
        preco_unidade,
        quantidade_por_unidade,
        nome_imagem
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
    
    # ==========================
    # ROTA: HISTÓRICO PRODUTO
    # ==========================
    @app.route(
    "/produto/detalhes/<int:produto_id>"
)
    def detalhes_produto_produto(produto_id):

        produto = pegar_produto_por_id(
        produto_id
    )

        historico = pegar_historico_preco(
        produto_id
    )

        return render_template(

        "produto/detalhes_produto.html",

        produto=produto,

        historico=historico
    )

