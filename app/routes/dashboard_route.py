from flask import render_template

def configurar_rotas_dashboard(app):

    @app.route("/dashboard")
    def dashboard():
        return render_template(
            "dashboard/dashboard.html",
            titulo_pagina="Dashboard"
        )