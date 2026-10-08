from flask import (
    render_template,
    session
)

from app.utils.auth import (
    login_obrigatorio
)

from app.controllers.dashboard_controller import (
    pegar_dashboard
)


def configurar_dashboard_routes(app):

    @app.route("/dashboard")
    @login_obrigatorio
    def dashboard():

        dados = pegar_dashboard()

        perfil = session.get(
            "perfil"
        )

        return render_template(
            "dashboard/dashboard.html",
            dados=dados,
            perfil=perfil
        )