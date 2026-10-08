# Importa as funções do model responsáveis
# por consultar informações relacionadas
# às contas pendentes no banco de dados.
from app.models.conta_model import (
    listar_contas_pendentes,
    buscar_conta_pendente_por_id,
    buscar_vendas_conta_pendente,
    buscar_produtos_venda,
    buscar_fichas_pendentes
)


# ==================================================
# LISTAR CONTAS PENDENTES
# ==================================================
#
# Solicita ao model todas as contas pendentes
# atualmente cadastradas no sistema.
#
# O retorno será utilizado para preencher
# a tela principal de contas pendentes.
#
# ==================================================

def pegar_contas():

    contas = listar_contas_pendentes()

    return contas


# ==================================================
# DETALHAR CONTA PENDENTE
# ==================================================
#
# Esta função monta toda a estrutura necessária
# para exibir a tela de detalhes de uma conta
# pendente.
#
# Fluxo:
#
# 1. Busca os dados principais da conta.
# 2. Busca todas as vendas vinculadas.
# 3. Calcula o valor total da conta.
# 4. Busca os produtos de cada venda.
# 5. Busca as fichas de sinuca de cada venda.
# 6. Agrupa tudo em uma única estrutura.
#
# O resultado final é enviado para o template
# responsável pela exibição dos detalhes.
#
# ==================================================

def pegar_detalhes_conta(conta_id):

    # Busca as informações principais da conta
    # utilizando o ID recebido pela rota.
    conta = buscar_conta_pendente_por_id(
        conta_id
    )

    # Busca todas as vendas associadas
    # à conta pendente selecionada.
    vendas = buscar_vendas_conta_pendente(
        conta_id
    )

    # Inicializa o valor total da conta.
    #
    # O valor será calculado somando todas
    # as vendas encontradas.
    conta["valor_total"] = 0

    # Percorre cada venda encontrada.
    for venda in vendas:

        # Soma o valor da venda ao total geral
        # da conta pendente.
        conta["valor_total"] += float(
            venda["valor_total"]
        )

        # Busca todos os produtos pertencentes
        # à venda atual.
        venda["produtos"] = buscar_produtos_venda(
            venda["id"]
        )

        # Busca as fichas de sinuca associadas
        # à venda atual.
        venda["fichas"] = buscar_fichas_pendentes(
            venda["id"]
        )

    # Adiciona a lista completa de vendas
    # dentro da estrutura da conta.
    #
    # Isso facilita a exibição das informações
    # no template.
    conta["vendas"] = vendas

    # Retorna todos os dados montados.
    return conta