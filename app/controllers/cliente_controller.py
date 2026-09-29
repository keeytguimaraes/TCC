# Importa flash
from flask import flash

# Importa funções do model cliente
from app.models.cliente_model import (
    listar_clientes,
    listar_clientes_inativos,
    cadastrar_cliente,
    desativar_cliente,
    reativar_cliente,
    editar_cliente,
    buscar_cliente_por_id,
    cliente_tem_conta_aberta,
    reativar_cliente
)

# ==========================
# LISTAR CLIENTES
# ==========================
def pegar_clientes():

    clientes = listar_clientes()

    for cliente in clientes:

        conta = cliente_tem_conta_aberta(
            cliente["id"]
        )

        if conta:

            cliente["conta_aberta"] = True

            cliente["saldo_devedor"] = (
                conta["saldo_devedor"]
            )

        else:

            cliente["conta_aberta"] = False

            cliente["saldo_devedor"] = 0

    return clientes

# ==========================
# CADASTRAR CLIENTE
# ==========================
def cadastrar_cliente_controller(nome):

    return cadastrar_cliente(nome)


# ==========================
# BUSCAR CLIENTE
# ==========================
def buscar_cliente_controller(id_cliente):

    return buscar_cliente_por_id(
        id_cliente
    )


# ==========================
# EDITAR CLIENTE
# ==========================
def editar_cliente_controller(

    id_cliente,
    nome

):

    editar_cliente(

        id_cliente,
        nome
    )


# ==========================
# DESATIVAR CLIENTE
# ==========================
def desativar_cliente_controller(
    id_cliente
):

    conta = cliente_tem_conta_aberta(
        id_cliente
    )

    # Se possuir conta aberta
    if conta:

        saldo = conta[
            "saldo_devedor"
        ]

        flash(
            f"Não é possível desativar o cliente. Saldo devedor atual: R$ {saldo:.2f}",
            "error"
        )

        return False

    # desativa cliente
    desativar_cliente(id_cliente)

    flash(
        "Cliente desativado com sucesso!",
        "success"
    )

    return True
def reativar_cliente_controller(
    id_cliente
):

    reativar_cliente(id_cliente)

    flash(
        "Cliente reativado com sucesso!",
        "success"
    )

# ==========================
# LISTAR CLIENTES INATIVOS
# ==========================
def listar_clientes_inativos_controller():

    return listar_clientes_inativos()