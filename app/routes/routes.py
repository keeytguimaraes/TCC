from app.utils.auth import (
    login_obrigatorio
)
from flask import render_template

def configurar_rotas(app):

    @app.route("/")
    @login_obrigatorio
    def home():

        return render_template(
            "dashboard/dashboard.html",
            titulo_pagina="Dashboard"
        )
    