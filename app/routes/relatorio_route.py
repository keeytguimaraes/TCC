from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)
from flask import (
    render_template,
    request
)

from app.controllers.relatorio_controller import (
    pegar_relatorio
)

from app.controllers.relatorio_pdf_controller import (
    pegar_vendas_periodo,
    pegar_resumo_periodo,
    pegar_fechamento_dia,
    pegar_resumo_fechamento
)

from app.utils.pdf_generator import (
    gerar_relatorio_vendas_pdf,
    gerar_fechamento_diario_pdf
)

from flask import send_file
from datetime import datetime

import os

from datetime import datetime

def configurar_relatorio_routes(app):

    @app.route("/relatorio")
    @login_obrigatorio
    @perfil_obrigatorio(
    "Administrador",
    "Gerente"
)
    def relatorio():

        dados = pegar_relatorio()

        return render_template(

            "relatorio/relatorio.html",

            dados=dados
        )
    
    @app.route("/relatorio/vendas")
    @login_obrigatorio
    @perfil_obrigatorio(
    "Administrador",
    "Gerente"
)
    def tela_relatorio_vendas():

        return render_template(
        "relatorio/vendas.html"
    )

    @app.route(
    "/relatorio/vendas/pdf",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "Administrador",
    "Gerente"
)
    def gerar_relatorio_vendas():

        data_inicial = request.form.get(
        "data_inicial"
    )

        data_final = request.form.get(
        "data_final"
    )
        
        tipo_vendas = request.form.get(
    "tipo_vendas"
)

        vendas = pegar_vendas_periodo(
        data_inicial,
    data_final,
    tipo_vendas
)

        resumo = pegar_resumo_periodo(
    data_inicial,
    data_final,
    tipo_vendas
)
        
        os.makedirs(
        "relatorios",
        exist_ok=True
    )

        timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

        caminho_pdf = (
    f"relatorios/relatorio_vendas_{timestamp}.pdf"
)
        gerar_relatorio_vendas_pdf(
    caminho_pdf,
    data_inicial,
    data_final,
    tipo_vendas,
    resumo,
    vendas
)

        return send_file(
    caminho_pdf,
    mimetype="application/pdf"
)
    
    @app.route(
    "/relatorio/fechamento"
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "Administrador",
    "Gerente"
)
    def tela_fechamento_diario():

        return render_template(
        "relatorio/fechamento_diario.html"
    )

    @app.route(
    "/relatorio/fechamento/pdf",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "Administrador",
    "Gerente"
)
    def gerar_fechamento_diario():

        data = request.form.get(
        "data"
    )

        vendas = pegar_fechamento_dia(
        data
    )

        resumo = pegar_resumo_fechamento(
        data
    )

        data_arquivo = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

        nome_arquivo = (
    f"fechamento_diario_"
    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
)

        caminho_pdf = (
    f"relatorios/{nome_arquivo}"
)

        gerar_fechamento_diario_pdf(
        caminho_pdf,
        data,
        resumo,
        vendas
    )

        return send_file(
        caminho_pdf,
        mimetype="application/pdf"
    )