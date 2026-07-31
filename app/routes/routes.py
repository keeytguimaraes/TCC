from flask import render_template


def configurar_rotas(app):

    @app.route("/")
    def home():

        return render_template(
            "dashboard/dashboard.html",
            titulo_pagina="Dashboard"
        )
    