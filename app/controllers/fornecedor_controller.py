# Importa as funções do model responsáveis
# pelas operações relacionadas aos fornecedores.
from app.models.fornecedor_model import (

    listar_fornecedores,
    cadastrar_fornecedor,
    buscar_fornecedor_por_id,
    editar_fornecedor,
    listar_fornecedores_inativos,
    reativar_fornecedor,
    desativar_fornecedor
)


# ==================================================
# LISTAR FORNECEDORES
# ==================================================
#
# Busca todos os fornecedores ativos
# cadastrados no sistema.
#
# Os dados retornados são utilizados
# para preencher a tabela principal
# da tela de fornecedores.
#
# ==================================================

def pegar_fornecedores():

    return listar_fornecedores()


# ==================================================
# CADASTRAR FORNECEDOR
# ==================================================
#
# Recebe os dados informados no formulário
# de cadastro e encaminha para o model.
#
# O controller não realiza validações
# nem acessa o banco diretamente.
#
# Fluxo:
#
# Route → Controller → Model → Banco
#
# ==================================================

def cadastrar_fornecedor_controller(

    nome,
    telefone,
    observacao
):

    cadastrar_fornecedor(

        nome,
        telefone,
        observacao
    )


# ==================================================
# BUSCAR FORNECEDOR POR ID
# ==================================================
#
# Busca um fornecedor específico
# utilizando seu identificador único.
#
# Esta função normalmente é utilizada
# na tela de edição ou visualização
# de detalhes.
#
# ==================================================

def pegar_fornecedor_por_id(

    id_fornecedor
):

    return buscar_fornecedor_por_id(
        id_fornecedor
    )


# ==================================================
# EDITAR FORNECEDOR
# ==================================================
#
# Recebe os novos dados informados
# pelo usuário e encaminha para
# o model realizar a atualização.
#
# ==================================================

def editar_fornecedor_controller(

    id_fornecedor,

    nome,
    telefone,
    observacao
):

    editar_fornecedor(

        id_fornecedor,

        nome,
        telefone,
        observacao
    )


# ==================================================
# LISTAR FORNECEDORES INATIVOS
# ==================================================
#
# Busca todos os fornecedores
# que foram desativados.
#
# Utilizado na tela de fornecedores
# inativos.
#
# ==================================================

def pegar_fornecedores_inativos():

    return listar_fornecedores_inativos()


# ==================================================
# REATIVAR FORNECEDOR
# ==================================================
#
# Reativa um fornecedor que havia
# sido desativado anteriormente.
#
# Após a reativação, ele volta
# a aparecer normalmente nas listas.
#
# ==================================================

def reativar_fornecedor_controller(
    id_fornecedor
):

    reativar_fornecedor(
        id_fornecedor
    )


# ==================================================
# DESATIVAR FORNECEDOR
# ==================================================
#
# Realiza a desativação lógica
# de um fornecedor.
#
# Os dados permanecem no banco,
# porém deixam de aparecer nas
# listagens principais.
#
# ==================================================

def desativar_fornecedor_controller(
    id_fornecedor
):

    desativar_fornecedor(
        id_fornecedor
    )