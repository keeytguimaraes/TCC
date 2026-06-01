# Importa função do model
from app.models.cliente_model import (
    listar_clientes,
    cadastrar_cliente,
    excluir_cliente,
    editar_cliente,
    buscar_cliente_por_id
)


# Controller responsável pelos clientes
def pegar_clientes():

    # Retorna lista de clientes do model
    return listar_clientes()
# Importa função de cadastro do model
from app.models.cliente_model import cadastrar_cliente


# Controller responsável por cadastrar cliente
def cadastrar_cliente_controller(nome):

    # Envia nome para o model
    return cadastrar_cliente(nome)
# Importa função de excluir
from app.models.cliente_model import excluir_cliente


# Controller responsável por excluir cliente
def excluir_cliente_controller(id_cliente):

    # Envia id para model
    excluir_cliente(id_cliente)
    # Controller responsável por buscar cliente
def buscar_cliente_controller(id_cliente):

    # Busca cliente
    return buscar_cliente_por_id(id_cliente)


# Controller responsável por editar cliente
def editar_cliente_controller(id_cliente, nome):

    # Envia dados para model
    editar_cliente(id_cliente, nome)