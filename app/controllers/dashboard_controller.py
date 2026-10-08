from flask import session

from app.models.dashboard_model import (
    buscar_dashboard_administrador,
    buscar_dashboard_gerente,
    buscar_dashboard_funcionario
)


def pegar_dashboard():

    perfil = session.get(
        "perfil"
    )

    if perfil == "administrador":

        return buscar_dashboard_administrador()

    elif perfil == "gerente":

        return buscar_dashboard_gerente()

    else:

        usuario_id = session.get(
            "usuario_id"
        )

        return buscar_dashboard_funcionario(
            usuario_id
        )