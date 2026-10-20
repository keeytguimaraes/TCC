
from flask import redirect, url_for


def configurar_rotas(app):
    """
    Registra as rotas gerais da aplicação.

    A rota inicial redireciona para o Dashboard oficial,
    que carrega os indicadores e demais dados do sistema.
    """

    @app.route("/")
    def home():
        # Direciona a página inicial para a rota oficial do Dashboard.
        return redirect(url_for("dashboard"))
