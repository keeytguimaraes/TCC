# Importa as funções do model responsáveis
# pelas operações relacionadas aos produtos.
from app.models.produto_model import (

    listar_produtos,

    listar_produtos_ativos,

    listar_produtos_inativos,

    cadastrar_produto,

    listar_categorias,

    buscar_produto_por_id,

    editar_produto,

    inativar_produto,

    ativar_produto,

    listar_produtos_venda,

    buscar_historico_preco
)


# ==================================================
# LISTAR CATEGORIAS
# ==================================================
#
# Busca todas as categorias cadastradas
# no sistema.
#
# Essas categorias são utilizadas nos
# formulários de cadastro e edição
# de produtos.
#
# ==================================================

def pegar_categorias():

    return listar_categorias()


# ==================================================
# LISTAR PRODUTOS
# ==================================================
#
# Busca todos os produtos cadastrados,
# independentemente do status.
#
# Utilizado principalmente na tela
# principal de gerenciamento de produtos.
#
# ==================================================

def pegar_produtos():

    return listar_produtos()


# ==================================================
# LISTAR PRODUTOS ATIVOS
# ==================================================
#
# Retorna apenas os produtos ativos.
#
# Produtos ativos são aqueles que podem
# ser utilizados normalmente no sistema.
#
# ==================================================

def pegar_produtos_ativos():

    return listar_produtos_ativos()


# ==================================================
# LISTAR PRODUTOS INATIVOS
# ==================================================
#
# Retorna os produtos que foram
# desativados pelo usuário.
#
# Utilizado na tela de produtos inativos.
#
# ==================================================

def pegar_produtos_inativos():

    return listar_produtos_inativos()


# ==================================================
# CADASTRAR PRODUTO
# ==================================================
#
# Recebe todos os dados preenchidos
# no formulário de cadastro de produto
# e encaminha para o model.
#
# O controller não realiza acesso ao banco.
#
# Fluxo:
#
# Route → Controller → Model → Banco
#
# ==================================================

def cadastrar_produto_controller(

    nome,

    categoria,

    sabor,

    tipo_embalagem,

    volume,

    preco_venda,

    preco_caixa,

    quantidade_por_caixa,

    estoque_minimo,

    vende_por_dose,

    vende_por_unidade,

    volume_dose_ml,

    preco_dose,

    preco_unidade,

    quantidade_por_unidade,

    imagem
):

    cadastrar_produto(

        nome,

        categoria,

        sabor,

        tipo_embalagem,

        volume,

        preco_venda,

        preco_caixa,

        quantidade_por_caixa,

        estoque_minimo,

        vende_por_dose,

        vende_por_unidade,

        volume_dose_ml,

        preco_dose,

        preco_unidade,

        quantidade_por_unidade,

        imagem
    )


# ==================================================
# BUSCAR PRODUTO POR ID
# ==================================================
#
# Busca um produto específico através
# do seu identificador único.
#
# Utilizado principalmente na edição
# e visualização de detalhes.
#
# ==================================================

def pegar_produto_por_id(

    produto_id
):

    return buscar_produto_por_id(
        produto_id
    )


# ==================================================
# EDITAR PRODUTO
# ==================================================
#
# Recebe os novos dados informados
# pelo usuário e encaminha para o model
# realizar a atualização.
#
# ==================================================

def editar_produto_controller(

    produto_id,

    nome,

    categoria,

    sabor,

    tipo_embalagem,

    volume,

    preco_venda,

    preco_caixa,

    quantidade_por_caixa,

    vende_por_dose,

    vende_por_unidade,

    volume_dose_ml,

    preco_dose,

    preco_unidade,

    quantidade_por_unidade
):

    editar_produto(

        produto_id,

        nome,

        categoria,

        sabor,

        tipo_embalagem,

        volume,

        preco_venda,

        preco_caixa,

        quantidade_por_caixa,

        vende_por_dose,

        vende_por_unidade,

        volume_dose_ml,

        preco_dose,

        preco_unidade,

        quantidade_por_unidade
    )


# ==================================================
# INATIVAR PRODUTO
# ==================================================
#
# Realiza a desativação lógica de um
# produto.
#
# O produto continua existindo no banco,
# mas deixa de aparecer nas listagens
# principais e vendas.
#
# ==================================================

def inativar_produto_controller(

    produto_id
):

    inativar_produto(
        produto_id
    )


# ==================================================
# ATIVAR PRODUTO
# ==================================================
#
# Reativa um produto anteriormente
# desativado.
#
# Após a ativação, o produto volta
# a ficar disponível no sistema.
#
# ==================================================

def ativar_produto_controller(

    produto_id
):

    ativar_produto(
        produto_id
    )


# ==================================================
# LISTAR PRODUTOS PARA VENDA
# ==================================================
#
# Retorna apenas os produtos que podem
# ser exibidos no PDV e utilizados
# durante uma venda.
#
# ==================================================

def pegar_produtos_venda():

    return listar_produtos_venda()


# ==================================================
# HISTÓRICO DE PREÇOS
# ==================================================
#
# Busca todas as alterações de preço
# realizadas em um produto.
#
# Utilizado para auditoria e consulta
# do histórico de valores.
#
# ==================================================

def pegar_historico_preco(produto_id):

    return buscar_historico_preco(
        produto_id
    )