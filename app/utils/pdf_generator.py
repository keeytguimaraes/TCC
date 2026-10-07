"""
SIGC - Gerador de PDF (Relatorio de Vendas + Fechamento Diario)

Camada de APRESENTACAO apenas. Nenhuma query, calculo ou regra de
negocio vive neste arquivo - os dados chegam prontos via os
parametros `resumo` e `vendas`, exatamente como antes.

As assinaturas publicas gerar_relatorio_vendas_pdf(...) e
gerar_fechamento_diario_pdf(...) permanecem identicas as versoes
anteriores: mesmos parametros, mesma ordem, mesmo comportamento de
escrita direta no arquivo. Nenhum outro modulo do projeto (rotas,
controllers, models) precisa ser alterado.

As duas funcoes compartilham a mesma paleta de cores e os mesmos
helpers de desenho (cabecalho, rodape, grade de indicadores, titulo
de secao), garantindo consistencia visual entre os dois relatorios.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from datetime import datetime


# ============================================================
# PALETA DE CORES (mesma paleta do Design System web do SIGC)
# ============================================================

COR_PRIMARIA        = colors.HexColor("#0F7A4F")
COR_PRIMARIA_CLARA  = colors.HexColor("#E6F4EE")

COR_SUCESSO         = colors.HexColor("#15803D")
COR_SUCESSO_CLARA   = colors.HexColor("#E7F6EC")

COR_ALERTA          = colors.HexColor("#B45309")
COR_ALERTA_CLARA    = colors.HexColor("#FEF3E2")

COR_TEXTO           = colors.HexColor("#111827")
COR_TEXTO_SECUNDARIO= colors.HexColor("#6B7280")
COR_TEXTO_TERCIARIO = colors.HexColor("#9CA3AF")

COR_BORDA           = colors.HexColor("#E5E7EB")
COR_FUNDO_SUAVE     = colors.HexColor("#FAFBFC")
COR_BRANCO          = colors.white


# ============================================================
# LAYOUT (tamanhos de pagina, margens e espacamentos)
# ============================================================

LARGURA_PAGINA, ALTURA_PAGINA = letter

MARGEM_ESQUERDA = 50
MARGEM_DIREITA  = 50
LARGURA_UTIL    = LARGURA_PAGINA - MARGEM_ESQUERDA - MARGEM_DIREITA

ALTURA_FAIXA_CABECALHO = 70
ALTURA_RODAPE          = 40
ALTURA_LINHA_TABELA    = 20
ALTURA_CABECALHO_TABELA= 22
ALTURA_CAIXA_KPI       = 50
ESPACO_KPI             = 10
ESPACO_SECAO           = 20
BUFFER_RODAPE          = 10

# Posicoes horizontais das colunas da tabela do RELATORIO DE VENDAS
# (4 colunas). Definidas uma unica vez e usadas tanto no cabecalho
# quanto nas linhas de dados, eliminando o desalinhamento que
# existia entre o cabecalho "STATUS" (x=430) e os dados (x=400).
COL_DATA_X     = MARGEM_ESQUERDA + 8
COL_CLIENTE_X  = MARGEM_ESQUERDA + 80
COL_VALOR_X    = MARGEM_ESQUERDA + 370
COL_STATUS_X   = MARGEM_ESQUERDA + 400

# Posicoes horizontais das colunas da tabela do FECHAMENTO DIARIO
# (6 colunas: HORA, CLIENTE, VALOR, RECEBIDO, TROCO, STATUS).
COL_HORA_X_FECH     = MARGEM_ESQUERDA + 8
COL_CLIENTE_X_FECH  = MARGEM_ESQUERDA + 45
COL_VALOR_X_FECH    = MARGEM_ESQUERDA + 280
COL_RECEBIDO_X_FECH = MARGEM_ESQUERDA + 350
COL_TROCO_X_FECH    = MARGEM_ESQUERDA + 410
COL_STATUS_X_FECH   = MARGEM_ESQUERDA + 420


# ============================================================
# FORMATACAO (identica a versao anterior)
# ============================================================

def moeda(valor):

    return (
        f"R$ {float(valor):.2f}"
        .replace(".", ",")
    )


# ============================================================
# FUNCOES AUXILIARES DE DESENHO (compartilhadas pelos 2 relatorios)
# ============================================================

def _status_cores(status):
    """
    Mapeia o status de pagamento (vindo do banco, sem alteracao)
    para a cor semantica correspondente do Design System.

    A comparacao e feita em minusculas porque, apos a migracao do
    projeto para PostgreSQL, o valor armazenado passou a ser
    'pago'/'pendente' (confirmado nas queries de
    relatorio_pdf_model.py). O texto exibido continua sendo
    exatamente venda["status_pagamento"], sem nenhuma alteracao -
    esta normalizacao serve apenas para escolher a cor certa do
    badge, e nao para mudar o que e mostrado.

    Qualquer valor nao mapeado cai em um tom neutro, para nunca
    quebrar a geracao do PDF se um status novo surgir no futuro.
    """

    status_normalizado = (status or "").strip().lower()

    if status_normalizado == "pago":
        return COR_SUCESSO, COR_SUCESSO_CLARA

    if status_normalizado == "pendente":
        return COR_ALERTA, COR_ALERTA_CLARA

    return COR_TEXTO_SECUNDARIO, COR_FUNDO_SUAVE


def _desenhar_cabecalho(pdf, titulo_documento="Relatorio de Vendas"):
    """
    Faixa de identidade visual. Chamada em TODAS as paginas
    (inclusive na pagina 2, 3...), corrigindo o bug em que "SIGC"
    so aparecia na primeira pagina.

    `titulo_documento` identifica, no canto direito da faixa, qual
    relatorio esta sendo exibido - "Relatorio de Vendas" (padrao,
    preserva o comportamento original) ou "Fechamento Diario".
    """

    pdf.setFillColor(COR_PRIMARIA)
    pdf.rect(
        0,
        ALTURA_PAGINA - ALTURA_FAIXA_CABECALHO,
        LARGURA_PAGINA,
        ALTURA_FAIXA_CABECALHO,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_BRANCO)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(MARGEM_ESQUERDA, ALTURA_PAGINA - 32, "SIGC")

    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        MARGEM_ESQUERDA,
        ALTURA_PAGINA - 48,
        "Sistema Integrado de Gestao Comercial"
    )

    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawRightString(
        LARGURA_PAGINA - MARGEM_DIREITA,
        ALTURA_PAGINA - 40,
        titulo_documento
    )

    return ALTURA_PAGINA - ALTURA_FAIXA_CABECALHO - ESPACO_SECAO


def _desenhar_metadados(pdf, y, campos):
    """
    Bloco de contexto do relatorio (ex: "Periodo"/"Filtro" no
    relatorio de vendas, ou apenas "Data" no fechamento diario),
    so desenhado na primeira pagina.

    `campos` e uma lista de ate 2 tuplas (rotulo, valor), exibidas
    lado a lado. Com 1 item, so a coluna esquerda e preenchida.
    """

    posicoes_x = [
        MARGEM_ESQUERDA,
        MARGEM_ESQUERDA + (LARGURA_UTIL / 2),
    ]

    pdf.setFillColor(COR_TEXTO_TERCIARIO)
    pdf.setFont("Helvetica-Bold", 8)

    for indice, (rotulo, _valor) in enumerate(campos):
        pdf.drawString(posicoes_x[indice], y, rotulo)

    y -= 14

    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica", 10)

    for indice, (_rotulo, valor) in enumerate(campos):
        pdf.drawString(posicoes_x[indice], y, valor)

    y -= 12

    pdf.setStrokeColor(COR_BORDA)
    pdf.setLineWidth(0.75)
    pdf.line(
        MARGEM_ESQUERDA,
        y,
        LARGURA_PAGINA - MARGEM_DIREITA,
        y
    )

    return y - ESPACO_SECAO


def _desenhar_titulo_secao(pdf, y, texto):
    """
    Titulo de secao com barra vertical na cor de marca, mesmo
    padrao visual ja usado nos cards de status do sistema web.
    """

    pdf.setFillColor(COR_PRIMARIA)
    pdf.rect(MARGEM_ESQUERDA, y - 9, 3, 11, fill=1, stroke=0)

    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(MARGEM_ESQUERDA + 10, y - 8, texto.upper())

    return y - ESPACO_SECAO


def _altura_grade_indicadores(qtd_indicadores):

    colunas = 3
    linhas = -(-qtd_indicadores // colunas)  # arredondamento para cima

    return (
        linhas * ALTURA_CAIXA_KPI
        + (linhas - 1) * ESPACO_KPI
        + ESPACO_SECAO
    )


def _desenhar_grade_indicadores(pdf, y, indicadores):
    """
    Desenha a grade de caixas de indicador (KPIs) a partir de uma
    lista ja pronta de tuplas (rotulo, valor, tom), onde tom e
    "sucesso" | "alerta" | "neutro". Usada tanto pelo relatorio de
    vendas quanto pelo fechamento diario.
    """

    colunas = 3
    largura_caixa = (
        LARGURA_UTIL - (colunas - 1) * ESPACO_KPI
    ) / colunas

    linhas = [
        indicadores[i:i + colunas]
        for i in range(0, len(indicadores), colunas)
    ]

    cores_valor = {
        "sucesso": COR_SUCESSO,
        "alerta": COR_ALERTA,
        "neutro": COR_TEXTO,
    }

    y_topo_grade = y

    for indice_linha, linha in enumerate(linhas):

        y_topo_caixa = y_topo_grade - indice_linha * (
            ALTURA_CAIXA_KPI + ESPACO_KPI
        )

        for indice_coluna, (label, valor, tom) in enumerate(linha):

            x = MARGEM_ESQUERDA + indice_coluna * (
                largura_caixa + ESPACO_KPI
            )

            pdf.setStrokeColor(COR_BORDA)
            pdf.setFillColor(COR_BRANCO)
            pdf.setLineWidth(0.75)
            pdf.rect(
                x,
                y_topo_caixa - ALTURA_CAIXA_KPI,
                largura_caixa,
                ALTURA_CAIXA_KPI,
                fill=1,
                stroke=1
            )

            pdf.setFillColor(COR_TEXTO_TERCIARIO)
            pdf.setFont("Helvetica-Bold", 7.5)
            pdf.drawString(x + 10, y_topo_caixa - 16, label)

            pdf.setFillColor(cores_valor[tom])
            pdf.setFont("Helvetica-Bold", 15)
            pdf.drawString(x + 10, y_topo_caixa - 36, valor)

    altura_grade = _altura_grade_indicadores(len(indicadores))

    return y_topo_grade - altura_grade


def _desenhar_estado_vazio(
    pdf,
    y,
    linha1="Nenhuma venda encontrada",
    linha2="para o periodo e filtro selecionados"
):
    """
    Exibido quando a lista de vendas esta vazia. Antes, a tabela
    simplesmente nao desenhava nada abaixo do cabecalho; agora
    comunica explicitamente que a busca rodou e nao encontrou
    resultados. Os textos sao parametrizaveis para se adequar ao
    contexto de cada relatorio (vendas por periodo vs. fechamento
    de um dia especifico).
    """

    altura_caixa = 60

    pdf.setStrokeColor(COR_BORDA)
    pdf.setLineWidth(0.75)
    pdf.rect(
        MARGEM_ESQUERDA,
        y - altura_caixa,
        LARGURA_UTIL,
        altura_caixa,
        fill=0,
        stroke=1
    )

    pdf.setFillColor(COR_TEXTO_TERCIARIO)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(
        LARGURA_PAGINA / 2,
        y - 28,
        linha1
    )

    pdf.setFont("Helvetica", 9)
    pdf.drawCentredString(
        LARGURA_PAGINA / 2,
        y - 42,
        linha2
    )


def _desenhar_rodape(pdf, pagina_atual, total_paginas, data_geracao):
    """
    Rodape com linha divisoria + 3 zonas (rastreabilidade, marca,
    paginacao). Chamado em TODAS as paginas pela funcao principal
    - corrigindo o bug em que o rodape so era desenhado uma vez,
    no final, aparecendo apenas na ultima pagina.
    """

    pdf.setStrokeColor(COR_BORDA)
    pdf.setLineWidth(0.75)
    pdf.line(
        MARGEM_ESQUERDA,
        ALTURA_RODAPE,
        LARGURA_PAGINA - MARGEM_DIREITA,
        ALTURA_RODAPE
    )

    pdf.setFillColor(COR_TEXTO_SECUNDARIO)
    pdf.setFont("Helvetica", 8)

    pdf.drawString(
        MARGEM_ESQUERDA,
        ALTURA_RODAPE - 14,
        f"Gerado em {data_geracao.strftime('%d/%m/%Y %H:%M')}"
    )

    pdf.drawCentredString(
        LARGURA_PAGINA / 2,
        ALTURA_RODAPE - 14,
        f"SIGC (c) {data_geracao.year}"
    )

    pdf.drawRightString(
        LARGURA_PAGINA - MARGEM_DIREITA,
        ALTURA_RODAPE - 14,
        f"Pagina {pagina_atual} de {total_paginas}"
    )

    # ============================================================
# RELATORIO DE VENDAS
# ============================================================

def _montar_indicadores(resumo, tipo_vendas):
    """
    Define QUAIS indicadores aparecem no resumo, preservando
    exatamente a mesma regra da versao anterior: o filtro "todas"
    mostra os 6 indicadores; ja o filtro "pagas"/"pendentes" mostra
    apenas Total de vendas e Ticket medio. Nenhum dado novo e
    exibido e nenhum e ocultado em relacao ao comportamento atual.
    """

    indicadores = [
        ("TOTAL DE VENDAS", str(resumo["total_vendas"]), "neutro"),
    ]

    if tipo_vendas == "todas":

        indicadores.append(
            ("PAGAS", str(resumo["pagas"]), "neutro")
        )
        indicadores.append(
            ("PENDENTES", str(resumo["pendentes"]), "neutro")
        )
        indicadores.append((
            "RECEBIDO",
            moeda(resumo["recebido"]),
            "sucesso" if resumo["recebido"] else "neutro"
        ))
        indicadores.append((
            "PENDENTE",
            moeda(resumo["pendente"]),
            "alerta" if resumo["pendente"] else "neutro"
        ))

    indicadores.append(
        ("TICKET MEDIO", moeda(resumo["ticket_medio"]), "neutro")
    )

    return indicadores


def _desenhar_resumo(pdf, y, resumo, tipo_vendas):

    y = _desenhar_titulo_secao(pdf, y, "Resumo")
    indicadores = _montar_indicadores(resumo, tipo_vendas)

    return _desenhar_grade_indicadores(pdf, y, indicadores)


def _desenhar_cabecalho_tabela(pdf, y):
    """
    Cabecalho da tabela do relatorio de vendas, com fundo colorido.
    Isolado em funcao propria para eliminar a duplicacao de codigo
    que existia na versao anterior (o mesmo bloco estava copiado
    dentro do tratamento de quebra de pagina).
    """

    pdf.setFillColor(COR_PRIMARIA_CLARA)
    pdf.rect(
        MARGEM_ESQUERDA,
        y - ALTURA_CABECALHO_TABELA + 6,
        LARGURA_UTIL,
        ALTURA_CABECALHO_TABELA,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_PRIMARIA)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(COL_DATA_X, y - 6, "DATA")
    pdf.drawString(COL_CLIENTE_X, y - 6, "CLIENTE")
    pdf.drawRightString(COL_VALOR_X, y - 6, "VALOR")
    pdf.drawString(COL_STATUS_X, y - 6, "STATUS")

    return y - ALTURA_CABECALHO_TABELA


def _desenhar_linha_tabela(pdf, venda, y, indice):
    """
    Uma linha de dados da tabela do relatorio de vendas. Mesma
    fonte de dados da versao anterior (venda["data_venda"],
    venda["cliente"], venda["valor_total"],
    venda["status_pagamento"]) - nenhum campo novo, nenhum campo
    removido.
    """

    if indice % 2 == 1:
        pdf.setFillColor(COR_FUNDO_SUAVE)
        pdf.rect(
            MARGEM_ESQUERDA,
            y - 14,
            LARGURA_UTIL,
            ALTURA_LINHA_TABELA,
            fill=1,
            stroke=0
        )

    data_formatada = venda["data_venda"].strftime("%d/%m/%Y")

    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(COL_DATA_X, y, data_formatada)
    pdf.drawString(COL_CLIENTE_X, y, venda["cliente"][:25])
    pdf.drawRightString(COL_VALOR_X, y, moeda(venda["valor_total"]))

    status_texto = venda["status_pagamento"]
    cor_texto, cor_fundo = _status_cores(status_texto)

    largura_badge = pdf.stringWidth(
        status_texto, "Helvetica-Bold", 7.5
    ) + 16

    pdf.setFillColor(cor_fundo)
    pdf.roundRect(
        COL_STATUS_X,
        y - 4,
        largura_badge,
        13,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(cor_texto)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawString(COL_STATUS_X + 8, y, status_texto)


def _calcular_total_paginas(qtd_vendas, tipo_vendas):
    """
    Estima o total de paginas ANTES de desenhar, usando as mesmas
    constantes de layout do desenho real, para permitir exibir
    "Pagina X de Y" em uma unica passada.
    """

    indicadores_exemplo = _montar_indicadores(
        {
            "total_vendas": 0,
            "pagas": 0,
            "pendentes": 0,
            "recebido": 0,
            "pendente": 0,
            "ticket_medio": 0,
        },
        tipo_vendas
    )

    altura_cabecalho  = ALTURA_FAIXA_CABECALHO + ESPACO_SECAO
    altura_metadados  = 14 + 12 + ESPACO_SECAO
    altura_titulo     = ESPACO_SECAO
    altura_grade      = _altura_grade_indicadores(len(indicadores_exemplo))

    y_apos_tabela_pagina1 = (
        ALTURA_PAGINA
        - altura_cabecalho
        - altura_metadados
        - altura_titulo
        - altura_grade
        - altura_titulo
        - ALTURA_CABECALHO_TABELA
    )

    linhas_pagina1 = max(
        1,
        int(
            (y_apos_tabela_pagina1 - ALTURA_RODAPE - BUFFER_RODAPE)
            / ALTURA_LINHA_TABELA
        )
    )

    y_apos_tabela_seguinte = (
        ALTURA_PAGINA
        - altura_cabecalho
        - altura_titulo
        - ALTURA_CABECALHO_TABELA
    )

    linhas_pagina_seguinte = max(
        1,
        int(
            (y_apos_tabela_seguinte - ALTURA_RODAPE - BUFFER_RODAPE)
            / ALTURA_LINHA_TABELA
        )
    )

    if qtd_vendas <= linhas_pagina1:
        return 1

    restantes = qtd_vendas - linhas_pagina1
    paginas_extras = -(-restantes // linhas_pagina_seguinte)

    return 1 + paginas_extras


def gerar_relatorio_vendas_pdf(
    caminho_pdf,
    data_inicial,
    data_final,
    tipo_vendas,
    resumo,
    vendas
):

    pdf = canvas.Canvas(caminho_pdf, pagesize=letter)
    pdf.setTitle("Relatorio de Vendas")

    data_inicial_formatada = datetime.strptime(
        data_inicial, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    data_final_formatada = datetime.strptime(
        data_final, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    filtro_label = {
        "todas": "Todas as vendas",
        "pagas": "Apenas Pagas",
        "pendentes": "Apenas Pendentes",
    }.get(tipo_vendas, "Todas as vendas")

    data_geracao = datetime.now()
    total_paginas = _calcular_total_paginas(len(vendas), tipo_vendas)
    pagina_atual = 1

    # ---- Primeira pagina: cabecalho + metadados + resumo + tabela ----

    y = _desenhar_cabecalho(pdf, "Relatorio de Vendas")
    y = _desenhar_metadados(
        pdf,
        y,
        [
            ("PERIODO", f"{data_inicial_formatada} ate {data_final_formatada}"),
            ("FILTRO", filtro_label),
        ]
    )
    y = _desenhar_resumo(pdf, y, resumo, tipo_vendas)
    y = _desenhar_titulo_secao(pdf, y, "Detalhamento")
    y = _desenhar_cabecalho_tabela(pdf, y)

    if not vendas:

        _desenhar_estado_vazio(pdf, y)

    else:

        for indice, venda in enumerate(vendas):

            limite_pagina = (
                ALTURA_RODAPE + ALTURA_LINHA_TABELA + BUFFER_RODAPE
            )

            if y < limite_pagina:

                _desenhar_rodape(
                    pdf, pagina_atual, total_paginas, data_geracao
                )

                pdf.showPage()
                pagina_atual += 1

                y = _desenhar_cabecalho(pdf, "Relatorio de Vendas")
                y = _desenhar_titulo_secao(
                    pdf, y, "Detalhamento (continuacao)"
                )
                y = _desenhar_cabecalho_tabela(pdf, y)

            _desenhar_linha_tabela(pdf, venda, y, indice)
            y -= ALTURA_LINHA_TABELA

    _desenhar_rodape(pdf, pagina_atual, total_paginas, data_geracao)

    pdf.save()

    # ============================================================
# FECHAMENTO DIARIO
# ============================================================

def _montar_indicadores_fechamento(resumo):
    """
    Define os indicadores do fechamento diario, na mesma ordem e
    com os mesmos 7 valores da versao anterior (nenhum dado novo,
    nenhum removido): total_vendas, total_vendido, total_pago,
    total_fiado, total_conta_pendente, total_troco, ticket_medio.

    A ordem original ja agrupa naturalmente por natureza do valor:
      Linha 1 -> volume e dinheiro que entrou (vendas/vendido/caixa)
      Linha 2 -> valores em aberto e saida de caixa (fiado/pendente/troco)
      Linha 3 -> media

    O "tom" de cada indicador e calculado a partir do PROPRIO VALOR
    ja fornecido pelo resumo (ex: troco negativo vira alerta) -
    nao e um dado novo, e so a cor de exibicao de um numero que ja
    existe.
    """

    total_pago  = resumo["total_pago"]
    total_fiado = resumo["total_fiado"]
    total_conta_pendente = resumo["total_conta_pendente"]
    total_troco = float(resumo["total_troco"])

    return [
        ("QUANTIDADE DE VENDAS", str(resumo["total_vendas"]), "neutro"),
        ("TOTAL VENDIDO", moeda(resumo["total_vendido"]), "neutro"),
        (
            "ENTROU NO CAIXA",
            moeda(total_pago),
            "sucesso" if total_pago else "neutro"
        ),
        (
            "FIADOS",
            moeda(total_fiado),
            "alerta" if total_fiado else "neutro"
        ),
        (
            "CONTAS PENDENTES",
            moeda(total_conta_pendente),
            "alerta" if total_conta_pendente else "neutro"
        ),
        (
            "TROCO CONCEDIDO",
            moeda(resumo["total_troco"]),
            "alerta" if total_troco < 0 else "neutro"
        ),
        ("TICKET MEDIO", moeda(resumo["ticket_medio"]), "neutro"),
    ]


def _desenhar_resumo_fechamento(pdf, y, resumo):

    y = _desenhar_titulo_secao(pdf, y, "Resumo do Dia")
    indicadores = _montar_indicadores_fechamento(resumo)

    return _desenhar_grade_indicadores(pdf, y, indicadores)


def _desenhar_cabecalho_tabela_fechamento(pdf, y):
    """
    Cabecalho da tabela do fechamento diario (6 colunas), com
    fundo colorido - mesmo tratamento visual do relatorio de
    vendas, adaptado para as colunas HORA/CLIENTE/VALOR/
    RECEBIDO/TROCO/STATUS.
    """

    pdf.setFillColor(COR_PRIMARIA_CLARA)
    pdf.rect(
        MARGEM_ESQUERDA,
        y - ALTURA_CABECALHO_TABELA + 6,
        LARGURA_UTIL,
        ALTURA_CABECALHO_TABELA,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_PRIMARIA)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(COL_HORA_X_FECH, y - 6, "HORA")
    pdf.drawString(COL_CLIENTE_X_FECH, y - 6, "CLIENTE")
    pdf.drawRightString(COL_VALOR_X_FECH, y - 6, "VALOR")
    pdf.drawRightString(COL_RECEBIDO_X_FECH, y - 6, "RECEBIDO")
    pdf.drawRightString(COL_TROCO_X_FECH, y - 6, "TROCO")
    pdf.drawString(COL_STATUS_X_FECH, y - 6, "STATUS")

    return y - ALTURA_CABECALHO_TABELA


def _desenhar_linha_tabela_fechamento(pdf, venda, y, indice):
    """
    Uma linha de dados da tabela do fechamento diario. Mesma fonte
    de dados da versao anterior (venda["data_venda"],
    venda["cliente"], venda["valor_total"],
    venda["valor_recebido"], venda["troco"],
    venda["status_pagamento"]) - nenhum campo novo, nenhum campo
    removido.

    O valor de TROCO recebe a cor de alerta quando negativo - o
    sinal ja vem do dado original, aqui so escolhemos a cor com
    base nele.
    """

    if indice % 2 == 1:
        pdf.setFillColor(COR_FUNDO_SUAVE)
        pdf.rect(
            MARGEM_ESQUERDA,
            y - 14,
            LARGURA_UTIL,
            ALTURA_LINHA_TABELA,
            fill=1,
            stroke=0
        )

    hora_formatada = venda["data_venda"].strftime("%H:%M")

    pdf.setFillColor(COR_TEXTO)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(COL_HORA_X_FECH, y, hora_formatada)
    pdf.drawString(COL_CLIENTE_X_FECH, y, venda["cliente"][:20])
    pdf.drawRightString(COL_VALOR_X_FECH, y, moeda(venda["valor_total"]))
    pdf.drawRightString(
        COL_RECEBIDO_X_FECH, y, moeda(venda["valor_recebido"])
    )

    troco_valor = float(venda["troco"])
    pdf.setFillColor(COR_ALERTA if troco_valor < 0 else COR_TEXTO)
    pdf.drawRightString(COL_TROCO_X_FECH, y, moeda(venda["troco"]))

    status_texto = venda["status_pagamento"]
    cor_texto, cor_fundo = _status_cores(status_texto)

    largura_badge = pdf.stringWidth(
        status_texto, "Helvetica-Bold", 7.5
    ) + 16

    pdf.setFillColor(cor_fundo)
    pdf.roundRect(
        COL_STATUS_X_FECH,
        y - 4,
        largura_badge,
        13,
        6,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(cor_texto)
    pdf.setFont("Helvetica-Bold", 7.5)
    pdf.drawString(COL_STATUS_X_FECH + 8, y, status_texto)


def _calcular_total_paginas_fechamento(qtd_vendas):
    """
    Mesma logica de _calcular_total_paginas, adaptada ao
    fechamento diario: o resumo sempre tem 7 indicadores fixos
    (sem variacao por filtro), entao a altura da grade e constante.
    """

    altura_cabecalho  = ALTURA_FAIXA_CABECALHO + ESPACO_SECAO
    altura_metadados  = 14 + 12 + ESPACO_SECAO
    altura_titulo     = ESPACO_SECAO
    altura_grade      = _altura_grade_indicadores(7)

    y_apos_tabela_pagina1 = (
        ALTURA_PAGINA
        - altura_cabecalho
        - altura_metadados
        - altura_titulo
        - altura_grade
        - altura_titulo
        - ALTURA_CABECALHO_TABELA
    )

    linhas_pagina1 = max(
        1,
        int(
            (y_apos_tabela_pagina1 - ALTURA_RODAPE - BUFFER_RODAPE)
            / ALTURA_LINHA_TABELA
        )
    )

    y_apos_tabela_seguinte = (
        ALTURA_PAGINA
        - altura_cabecalho
        - altura_titulo
        - ALTURA_CABECALHO_TABELA
    )

    linhas_pagina_seguinte = max(
        1,
        int(
            (y_apos_tabela_seguinte - ALTURA_RODAPE - BUFFER_RODAPE)
            / ALTURA_LINHA_TABELA
        )
    )

    if qtd_vendas <= linhas_pagina1:
        return 1

    restantes = qtd_vendas - linhas_pagina1
    paginas_extras = -(-restantes // linhas_pagina_seguinte)

    return 1 + paginas_extras


def gerar_fechamento_diario_pdf(
    caminho_pdf,
    data,
    resumo,
    vendas
):

    pdf = canvas.Canvas(caminho_pdf, pagesize=letter)
    pdf.setTitle("Fechamento Diario")

    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    data_geracao = datetime.now()
    total_paginas = _calcular_total_paginas_fechamento(len(vendas))
    pagina_atual = 1

    # ---- Primeira pagina: cabecalho + data + resumo + tabela ----

    y = _desenhar_cabecalho(pdf, "Fechamento Diario")
    y = _desenhar_metadados(pdf, y, [("DATA", data_formatada)])
    y = _desenhar_resumo_fechamento(pdf, y, resumo)
    y = _desenhar_titulo_secao(pdf, y, "Detalhamento")
    y = _desenhar_cabecalho_tabela_fechamento(pdf, y)

    if not vendas:

        _desenhar_estado_vazio(
            pdf,
            y,
            "Nenhuma venda registrada",
            "para a data selecionada"
        )

    else:

        for indice, venda in enumerate(vendas):

            limite_pagina = (
                ALTURA_RODAPE + ALTURA_LINHA_TABELA + BUFFER_RODAPE
            )

            if y < limite_pagina:

                _desenhar_rodape(
                    pdf, pagina_atual, total_paginas, data_geracao
                )

                pdf.showPage()
                pagina_atual += 1

                y = _desenhar_cabecalho(pdf, "Fechamento Diario")
                y = _desenhar_titulo_secao(
                    pdf, y, "Detalhamento (continuacao)"
                )
                y = _desenhar_cabecalho_tabela_fechamento(pdf, y)

            _desenhar_linha_tabela_fechamento(pdf, venda, y, indice)
            y -= ALTURA_LINHA_TABELA

    _desenhar_rodape(pdf, pagina_atual, total_paginas, data_geracao)

    pdf.save()