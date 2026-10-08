# Importa a sessão do Flask.
#
# A sessão armazena informações do usuário
# que realizou login no sistema.
from flask import session


# Importa as funções responsáveis por montar
# os dados do dashboard de cada perfil.
from app.models.dashboard_model import (
    buscar_dashboard_administrador,
    buscar_dashboard_gerente,
    buscar_dashboard_funcionario
)


# ==================================================
# CARREGAR DASHBOARD
# ==================================================
#
# Esta função identifica o perfil do usuário
# atualmente logado e retorna os dados
# correspondentes ao dashboard adequado.
#
# Perfis disponíveis:
#
# - Administrador
# - Gerente
# - Funcionário
#
# Cada perfil possui informações diferentes
# exibidas na tela inicial do sistema.
#
# Fluxo:
#
# 1. Obtém o perfil da sessão.
# 2. Verifica qual perfil está logado.
# 3. Busca os dados correspondentes.
# 4. Retorna os dados para a rota.
#
# ==================================================

def pegar_dashboard():

    # Obtém da sessão o perfil do usuário
    # que realizou login.
    perfil = session.get(
        "perfil"
    )

    # Se o usuário for administrador,
    # carrega o dashboard completo.
    if perfil == "administrador":

        return buscar_dashboard_administrador()

    # Se o usuário for gerente,
    # carrega o dashboard do gerente.
    elif perfil == "gerente":

        return buscar_dashboard_gerente()

    # Caso não seja administrador
    # nem gerente, considera-se
    # o perfil de funcionário.
    else:

        # Obtém o ID do usuário logado.
        #
        # Esse ID será utilizado para
        # buscar apenas as informações
        # relacionadas ao próprio funcionário.
        usuario_id = session.get(
            "usuario_id"
        )

        # Retorna o dashboard individual
        # do funcionário.
        return buscar_dashboard_funcionario(
            usuario_id
        )