from app.utils.auth import (
    login_obrigatorio
)
from flask import render_template

def configurar_rotas_dashboard(app):

    @app.route("/dashboard")
    @login_obrigatorio
    def dashboard():
        return render_template(
            "dashboard/dashboard.html",
            titulo_pagina="Dashboard"
        )