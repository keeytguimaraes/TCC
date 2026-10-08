# Importa a função flash do Flask.
#
# Ela é utilizada para exibir mensagens
# temporárias ao usuário após determinadas
# operações do sistema.
from flask import flash


# Importa todas as funções responsáveis
# pela comunicação com a tabela de clientes
# no banco de dados.
from app.models.cliente_model import (
    listar_clientes,
    listar_clientes_inativos,
    cadastrar_cliente,
    desativar_cliente,
    reativar_cliente,
    editar_cliente,
    buscar_cliente_por_id,
    cliente_tem_conta_aberta
)


# ==================================================
# LISTAR CLIENTES
# ==================================================
#
# Solicita ao model todos os clientes ativos
# cadastrados no sistema.
#
# O resultado será utilizado para preencher
# a tabela exibida na tela de clientes.
#
# ==================================================

def pegar_clientes():

    return listar_clientes()


# ==================================================
# CADASTRAR CLIENTE
# ==================================================
#
# Recebe o nome informado pelo usuário
# e encaminha para o model realizar
# o cadastro no banco de dados.
#
# ==================================================

def cadastrar_cliente_controller(nome):

    return cadastrar_cliente(nome)


# ==================================================
# BUSCAR CLIENTE POR ID
# ==================================================
#
# Localiza um cliente específico através
# do ID recebido pela rota.
#
# Normalmente utilizado para preencher
# formulários de edição.
#
# ==================================================

def buscar_cliente_controller(id_cliente):

    return buscar_cliente_por_id(
        id_cliente
    )


# ==================================================
# EDITAR CLIENTE
# ==================================================
#
# Atualiza os dados de um cliente já
# existente no banco de dados.
#
# ==================================================

def editar_cliente_controller(
    id_cliente,
    nome
):

    editar_cliente(
        id_cliente,
        nome
    )


# ==================================================
# DESATIVAR CLIENTE
# ==================================================
#
# Antes de desativar um cliente,
# o sistema verifica se ele possui
# alguma conta em aberto.
#
# Caso exista saldo devedor,
# a desativação é bloqueada.
#
# Isso evita que clientes com dívidas
# desapareçam das operações financeiras.
#
# ==================================================

def desativar_cliente_controller(
    id_cliente
):

    # Verifica se existe alguma conta
    # financeira aberta para este cliente.
    conta = cliente_tem_conta_aberta(
        id_cliente
    )

    # Caso exista uma conta aberta,
    # impede a desativação.
    if conta:

        saldo = conta["saldo_devedor"]

        flash(
            f"Não é possível desativar o cliente. Saldo devedor atual: R$ {saldo:.2f}",
            "error"
        )

        return False

    # Se não existir pendência financeira,
    # o cliente pode ser desativado.
    desativar_cliente(id_cliente)

    flash(
        "Cliente desativado com sucesso!",
        "success"
    )

    return True


# ==================================================
# REATIVAR CLIENTE
# ==================================================
#
# Reativa um cliente anteriormente
# desativado no sistema.
#
# ==================================================

def reativar_cliente_controller(
    id_cliente
):

    reativar_cliente(id_cliente)

    flash(
        "Cliente reativado com sucesso!",
        "success"
    )


# ==================================================
# LISTAR CLIENTES INATIVOS
# ==================================================
#
# Retorna todos os clientes que estão
# marcados como inativos no sistema.
#
# ==================================================

def listar_clientes_inativos_controller():

    return listar_clientes_inativos()