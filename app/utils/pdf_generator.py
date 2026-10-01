from reportlab.pdfgen import canvas
from datetime import datetime



def moeda(valor):

    return (
        f"R$ {float(valor):.2f}"
        .replace(".", ",")
    )

def gerar_relatorio_vendas_pdf(
    caminho_pdf,
    data_inicial,
    data_final,
    tipo_vendas,
    resumo,
    vendas
):

    pdf = canvas.Canvas(
        caminho_pdf
    )

    pdf.setTitle(
        "Relatorio de Vendas"
    )

    y = 800

    # Título

    pdf.setFont(
        "Helvetica-Bold",
        16
    )

    pdf.drawString(
        50,
        y,
        "SIGC"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        "Sistema Integrado de Gestao Comercial"
    )

    y -= 40

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "RELATORIO DE VENDAS"
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        11
    )

    data_inicial_formatada = (
    datetime.strptime(
        data_inicial,
        "%Y-%m-%d"
    ).strftime(
        "%d/%m/%Y"
    )
)

    data_final_formatada = (
    datetime.strptime(
        data_final,
        "%Y-%m-%d"
    ).strftime(
        "%d/%m/%Y"
    )
)
    
    pdf.drawString(
    50,
    y,
    (
        f"Periodo: "
        f"{data_inicial_formatada}"
        f" ate "
        f"{data_final_formatada}"
    )
)

    y -= 20

    filtro = {
    "todas": "Todas as vendas",
    "pagas": "Apenas Pagas",
    "pendentes": "Apenas Pendentes"
}.get(
    tipo_vendas,
    "Todas as vendas"
)

    pdf.drawString(
    50,
    y,
    f"Filtro: {filtro}"
)
    
    y -= 40

    # Resumo

    pdf.setFont(
        "Helvetica-Bold",
        12
    )

    pdf.drawString(
        50,
        y,
        "RESUMO"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"Total de vendas: {resumo['total_vendas']}"
    )

    y -= 20

    if tipo_vendas == "todas":

        pdf.drawString(
        50,
        y,
        f"Pagas: {resumo['pagas']}"
    )

        y -= 20

        pdf.drawString(
        50,
        y,
        f"Pendentes: {resumo['pendentes']}"
    )

    y -= 20

    if tipo_vendas == "todas":

        pdf.drawString(
        50,
        y,
        f"Recebido: {moeda(resumo['recebido'])}"
    )

        y -= 20

        pdf.drawString(
        50,
        y,
        f"Pendente: {moeda(resumo['pendente'])}"
    )
        
    y -= 20

    pdf.drawString(
        50,
        y,
        f"Ticket medio: {moeda(resumo['ticket_medio'])}"
    )

    y -= 40

    # Tabela

    pdf.setFont(
        "Helvetica-Bold",
        10
    )

    pdf.drawString(
    40,
    y,
    "DATA"
)

    pdf.drawString(
    120,
    y,
    "CLIENTE"
)

    pdf.drawString(
    300,
    y,
    "VALOR"
)

    pdf.drawString(
    430,
    y,
    "STATUS"
)

    y -= 20

    pdf.setFont(
        "Helvetica",
        9
    )

    for venda in vendas:

        data_formatada = venda[
    "data_venda"
].strftime(
    "%d/%m/%Y"
)
        
        pdf.drawString(
    40,
    y,
    data_formatada
)

        pdf.drawString(
    120,
    y,
    venda["cliente"][:25]
)

        pdf.drawString(
            300,
            y,
           moeda(venda["valor_total"])
        )

        pdf.drawString(
            400,
            y,
            venda["status_pagamento"]
        )

        y -= 18

        if y < 50:

            pdf.showPage()

            y = 800

            pdf.setFont(
        "Helvetica-Bold",
        14
    )

            pdf.drawString(
        50,
        y,
        "RELATORIO DE VENDAS"
    )

            y -= 30

            pdf.setFont(
        "Helvetica-Bold",
        10
    )

            pdf.drawString(
        40,
        y,
        "DATA"
    )

            pdf.drawString(
        120,
        y,
        "CLIENTE"
    )

            pdf.drawString(
        300,
        y,
        "VALOR"
    )

            pdf.drawString(
        430,
        y,
        "STATUS"
    )

            y -= 20

            pdf.setFont(
        "Helvetica",
        9
    )

    data_geracao = datetime.now()

    pdf.drawString(
    50,
    30,
    (
        "Relatorio gerado em "
        + data_geracao.strftime(
            "%d/%m/%Y %H:%M"
        )
    )
)
    
    pagina = pdf.getPageNumber()

    pdf.drawRightString(
    550,
    30,
    f"Pagina {pagina}"
)

    pdf.save()