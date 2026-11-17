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
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import io
from datetime import datetime


# ============================================================
# PALETA DE CORES (identidade SIGC: preto, vermelho e amarelo)
# ============================================================

# Identidade principal
COR_PRETO           = colors.HexColor("#1F1F1F")
COR_PRIMARIA        = colors.HexColor("#C62828")   # vermelho SIGC
COR_PRIMARIA_CLARA  = colors.HexColor("#F3F1ED")   # fundo neutro de cabecalho de tabela
COR_AMARELO         = colors.HexColor("#FBC02D")   # amarelo SIGC (detalhe)

# Cores semanticas (mesmas do sistema web)
COR_SUCESSO         = colors.HexColor("#2E7D32")
COR_SUCESSO_CLARA   = colors.HexColor("#E8F3E9")

COR_ALERTA          = colors.HexColor("#7A5600")
COR_ALERTA_CLARA    = colors.HexColor("#FFF3CD")

COR_FIADO           = colors.HexColor("#1E4FA3")
COR_FIADO_CLARA     = colors.HexColor("#E3EDFB")

COR_TEXTO           = colors.HexColor("#1F1F1F")
COR_TEXTO_SECUNDARIO= colors.HexColor("#6B6B6B")
COR_TEXTO_TERCIARIO = colors.HexColor("#8A8A8A")

COR_BORDA           = colors.HexColor("#E3E0DA")
COR_FUNDO_SUAVE     = colors.HexColor("#F7F6F4")
COR_BRANCO          = colors.white


# ============================================================
# LAYOUT (tamanhos de pagina, margens e espacamentos)
# ============================================================

LARGURA_PAGINA, ALTURA_PAGINA = A4   # A4 (210 x 297 mm)

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

# Tabelas: cada coluna e (titulo, largura em pontos, alinhamento).
# A coluna "CLIENTE" (largura None) recebe todo o espaco que sobra, de
# modo que a soma das colunas e SEMPRE igual a area util da pagina.
# Cabecalho e celulas usam as mesmas posicoes (calculadas uma unica
# vez em _posicoes_colunas), entao nunca ficam desalinhados.
PADDING_CELULA = 8      # espaco horizontal interno de cada celula
ENTRELINHA     = 11     # altura de cada linha de texto dentro da celula
TAM_FONTE_CELULA = 9

COLUNAS_VENDAS = [
    ("DATA",    72,   "esq"),
    ("CLIENTE", None, "esq"),
    ("VALOR",   96,   "dir"),
    ("STATUS",  84,   "esq"),
]

COLUNAS_DESEMPENHO = [
    ("FUNCIONÁRIO",   None, "esq"),
    ("VENDAS",        70,   "dir"),
    ("TOTAL VENDIDO", 110,  "dir"),
    ("TICKET MÉDIO",  100,  "dir"),
]

COLUNAS_FECHAMENTO = [
    ("HORA",     40,   "esq"),
    ("CLIENTE",  None, "esq"),
    ("VALOR",    78,   "dir"),
    ("RECEBIDO", 80,   "dir"),
    ("TROCO",    74,   "dir"),
    ("STATUS",   66,   "esq"),
]


# ============================================================
# FORMATACAO (identica a versao anterior)
# ============================================================

def moeda(valor):

    # Mesmo valor e mesmo arredondamento de antes; apenas passa a
    # usar ponto como separador de milhar (1.234,50).
    return (
        "R$ " + f"{float(valor):,.2f}"
        .replace(",", "#")
        .replace(".", ",")
        .replace("#", ".")
    )


def _quebrar_texto(pdf, texto, fonte, tamanho, largura_max):
    """
    Quebra automatica de linha: devolve a lista de linhas que cabem em
    `largura_max` pontos. Nada e cortado nem substituido por
    reticencias; palavras maiores que a coluna sao divididas.
    """

    texto = "" if texto is None else str(texto)

    if not texto.strip():
        return [""]

    linhas = []
    atual = ""

    for palavra in texto.split():

        candidata = palavra if not atual else atual + " " + palavra

        if pdf.stringWidth(candidata, fonte, tamanho) <= largura_max:
            atual = candidata
            continue

        if atual:
            linhas.append(atual)
            atual = ""

        # palavra sozinha maior que a coluna: divide por caracteres
        while pdf.stringWidth(palavra, fonte, tamanho) > largura_max:
            corte = len(palavra) - 1
            while corte > 1 and pdf.stringWidth(
                palavra[:corte], fonte, tamanho
            ) > largura_max:
                corte -= 1
            linhas.append(palavra[:corte])
            palavra = palavra[corte:]

        atual = palavra

    if atual:
        linhas.append(atual)

    return linhas


def _tamanho_que_cabe(pdf, texto, fonte, tamanho, largura_max):
    """Reduz a fonte (so se preciso) para o texto caber na largura."""

    while tamanho > 6 and pdf.stringWidth(texto, fonte, tamanho) > largura_max:
        tamanho -= 0.5

    return tamanho


def _posicoes_colunas(colunas):
    """Devolve [(x_esquerda, largura)] com a soma == LARGURA_UTIL."""

    fixas = sum(c[1] for c in colunas if c[1] is not None)
    flexivel = LARGURA_UTIL - fixas

    posicoes = []
    x = MARGEM_ESQUERDA

    for _titulo, largura, _alinh in colunas:

        largura = flexivel if largura is None else largura
        posicoes.append((x, largura))
        x += largura

    return posicoes


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

    if status_normalizado == "fiado":
        return COR_FIADO, COR_FIADO_CLARA

    return COR_TEXTO_SECUNDARIO, COR_FUNDO_SUAVE


def _desenhar_cabecalho(pdf, titulo_documento="Relatório de Vendas"):
    """
    Faixa de identidade visual. Chamada em TODAS as paginas
    (inclusive na pagina 2, 3...), corrigindo o bug em que "SIGC"
    so aparecia na primeira pagina.

    `titulo_documento` identifica, no canto direito da faixa, qual
    relatorio esta sendo exibido - "Relatorio de Vendas" (padrao,
    preserva o comportamento original) ou "Fechamento Diario".
    """

    # faixa preta + filete vermelho com detalhe amarelo na base
    pdf.setFillColor(COR_PRETO)
    pdf.rect(
        0,
        ALTURA_PAGINA - ALTURA_FAIXA_CABECALHO,
        LARGURA_PAGINA,
        ALTURA_FAIXA_CABECALHO,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_PRIMARIA)
    pdf.rect(
        0,
        ALTURA_PAGINA - ALTURA_FAIXA_CABECALHO,
        LARGURA_PAGINA,
        4,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_AMARELO)
    pdf.rect(
        MARGEM_ESQUERDA,
        ALTURA_PAGINA - ALTURA_FAIXA_CABECALHO,
        60,
        4,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_BRANCO)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(MARGEM_ESQUERDA, ALTURA_PAGINA - 32, "SIGC")

    pdf.setFillColor(colors.HexColor("#C9C6BF"))
    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        MARGEM_ESQUERDA,
        ALTURA_PAGINA - 48,
        "Sistema Integrado de Gestão Comercial"
    )

    pdf.setFillColor(COR_BRANCO)
    pdf.setFont("Helvetica-Bold", 12)
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

            cor_barra = {
                "sucesso": COR_SUCESSO,
                "alerta": COR_AMARELO,
                "neutro": COR_PRETO,
            }[tom]

            pdf.setFillColor(cor_barra)
            pdf.rect(
                x,
                y_topo_caixa - ALTURA_CAIXA_KPI,
                3,
                ALTURA_CAIXA_KPI,
                fill=1,
                stroke=0
            )

            pdf.setFillColor(COR_TEXTO_SECUNDARIO)
            pdf.setFont("Helvetica-Bold", 7.5)
            pdf.drawString(x + 12, y_topo_caixa - 16, label)

            pdf.setFillColor(cores_valor[tom])
            pdf.setFont(
                "Helvetica-Bold",
                _tamanho_que_cabe(
                    pdf, valor, "Helvetica-Bold", 15, largura_caixa - 20
                )
            )
            pdf.drawString(x + 12, y_topo_caixa - 36, valor)

    altura_grade = _altura_grade_indicadores(len(indicadores))

    return y_topo_grade - altura_grade


def _desenhar_estado_vazio(
    pdf,
    y,
    linha1="Nenhuma venda encontrada",
    linha2="para o período e filtro selecionados"
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
        f"SIGC © {data_geracao.year}"
    )

    pdf.drawRightString(
        LARGURA_PAGINA - MARGEM_DIREITA,
        ALTURA_RODAPE - 14,
        f"Página {pagina_atual} de {total_paginas}"
    )

def _desenhar_tabela(
    pdf, y, vendas, colunas, celulas_da_venda,
    titulo_documento, pagina_atual, total_paginas, data_geracao,
    cabecalho_tabela
):
    """
    Desenha as linhas com quebra de pagina automatica. Repete cabecalho
    do documento, titulo de secao e cabecalho da tabela a cada pagina e
    desenha o rodape em todas. Devolve a ultima pagina usada.
    `y` e o topo da primeira linha.
    """

    limite_inferior = ALTURA_RODAPE + BUFFER_RODAPE
    primeira_da_pagina = True

    for indice, venda in enumerate(vendas):

        linhas_cliente = _linhas_cliente(pdf, venda, colunas)
        altura = _altura_linha(pdf, venda, colunas)

        if y - altura < limite_inferior and not primeira_da_pagina:

            _desenhar_rodape(
                pdf, pagina_atual, total_paginas, data_geracao
            )

            pdf.showPage()
            pagina_atual += 1

            y = _desenhar_cabecalho(pdf, titulo_documento)
            y = _desenhar_titulo_secao(
                pdf, y, "Detalhamento (continuação)"
            )
            y = cabecalho_tabela(pdf, y)
            primeira_da_pagina = True

        _desenhar_linha(
            pdf, colunas, celulas_da_venda(venda),
            linhas_cliente, y, altura, indice
        )

        y -= altura
        primeira_da_pagina = False

    return pagina_atual


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
        ("TICKET MÉDIO", moeda(resumo["ticket_medio"]), "neutro")
    )

    return indicadores


def _desenhar_resumo(pdf, y, resumo, tipo_vendas):

    y = _desenhar_titulo_secao(pdf, y, "Resumo")
    indicadores = _montar_indicadores(resumo, tipo_vendas)

    return _desenhar_grade_indicadores(pdf, y, indicadores)


def _desenhar_cabecalho_tabela(pdf, y, colunas=None):
    """
    Cabecalho de tabela (mesmo visual de antes). `y` e a linha-base
    onde o cabecalho comeca; devolve o Y do TOPO da primeira linha de
    dados. Titulos usam as mesmas posicoes/alinhamentos das celulas.
    """

    colunas = COLUNAS_VENDAS if colunas is None else colunas

    pdf.setFillColor(COR_PRIMARIA_CLARA)
    pdf.rect(
        MARGEM_ESQUERDA,
        y - ALTURA_CABECALHO_TABELA + 6,
        LARGURA_UTIL,
        ALTURA_CABECALHO_TABELA,
        fill=1,
        stroke=0
    )

    pdf.setFillColor(COR_TEXTO_SECUNDARIO)
    pdf.setFont("Helvetica-Bold", 8.5)

    for (titulo, _l, alinh), (x, largura) in zip(
        colunas, _posicoes_colunas(colunas)
    ):
        if alinh == "dir":
            pdf.drawRightString(x + largura - PADDING_CELULA, y - 8, titulo)
        else:
            pdf.drawString(x + PADDING_CELULA, y - 8, titulo)

    return y - ALTURA_CABECALHO_TABELA + 6


def _linhas_cliente(pdf, venda, colunas):
    """
    Linhas (apos quebra automatica) do texto da coluna que quebra
    linha: "CLIENTE" (venda["cliente"]) nos relatorios de vendas e
    "FUNCIONÁRIO" (venda["funcionario"]) no desempenho de funcionarios.
    """

    posicoes = _posicoes_colunas(colunas)
    titulos = [c[0] for c in colunas]

    if "CLIENTE" in titulos:
        indice, campo = titulos.index("CLIENTE"), "cliente"
    else:
        indice, campo = titulos.index("FUNCIONÁRIO"), "funcionario"

    largura = posicoes[indice][1] - 2 * PADDING_CELULA

    return _quebrar_texto(
        pdf, venda[campo], "Helvetica", TAM_FONTE_CELULA, largura
    )


def _altura_linha(pdf, venda, colunas):
    """Altura da linha: cresce se o nome do cliente ocupar varias linhas."""

    qtd = len(_linhas_cliente(pdf, venda, colunas))

    return max(ALTURA_LINHA_TABELA, qtd * ENTRELINHA + 9)


def _desenhar_linha(pdf, colunas, celulas, linhas_cliente, y_topo, altura, indice):
    """
    Desenha UMA linha de tabela. `celulas` traz, na ordem das colunas,
    (tipo, valor, cor) com tipo "texto" | "cliente" | "numero" | "status".
    O fundo alternado cobre a largura toda e a altura real da linha.
    """

    if indice % 2 == 1:
        pdf.setFillColor(COR_FUNDO_SUAVE)
        pdf.rect(
            MARGEM_ESQUERDA,
            y_topo - altura,
            LARGURA_UTIL,
            altura,
            fill=1,
            stroke=0
        )

    base = y_topo - 13   # linha-base da 1a linha de texto (centrada na linha minima)

    for (tipo, valor, cor), (x, largura) in zip(
        celulas, _posicoes_colunas(colunas)
    ):
        disponivel = largura - 2 * PADDING_CELULA

        if tipo == "cliente":

            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica", TAM_FONTE_CELULA)

            for i, linha in enumerate(linhas_cliente):
                pdf.drawString(
                    x + PADDING_CELULA, base - i * ENTRELINHA, linha
                )

        elif tipo == "numero":

            tamanho = _tamanho_que_cabe(
                pdf, valor, "Helvetica", TAM_FONTE_CELULA, disponivel
            )
            pdf.setFillColor(cor)
            pdf.setFont("Helvetica", tamanho)
            pdf.drawRightString(x + largura - PADDING_CELULA, base, valor)

        elif tipo == "status":

            cor_texto, cor_fundo = _status_cores(valor)

            tamanho = _tamanho_que_cabe(
                pdf, valor, "Helvetica-Bold", 7.5, disponivel - 16
            )
            largura_badge = pdf.stringWidth(
                valor, "Helvetica-Bold", tamanho
            ) + 16

            pdf.setFillColor(cor_fundo)
            pdf.roundRect(
                x + PADDING_CELULA,
                base - 4,
                largura_badge,
                13,
                6,
                fill=1,
                stroke=0
            )

            pdf.setFillColor(cor_texto)
            pdf.setFont("Helvetica-Bold", tamanho)
            pdf.drawString(x + PADDING_CELULA + 8, base, valor)

        else:

            pdf.setFillColor(COR_TEXTO)
            pdf.setFont("Helvetica", TAM_FONTE_CELULA)
            pdf.drawString(x + PADDING_CELULA, base, valor)


def _celulas_vendas(venda):
    """Mesmos campos de antes: data, cliente, valor_total, status_pagamento."""

    return [
        ("texto", venda["data_venda"].strftime("%d/%m/%Y"), None),
        ("cliente", None, None),
        ("numero", moeda(venda["valor_total"]), COR_TEXTO),
        ("status", venda["status_pagamento"], None),
    ]



def _montar_relatorio_vendas(
    pdf, total_paginas, data_geracao,
    data_inicial_formatada, data_final_formatada, filtro_label,
    tipo_vendas, resumo, vendas
):
    """Desenha o documento inteiro e devolve o numero de paginas usadas."""

    pagina_atual = 1

    # ---- Primeira pagina: cabecalho + metadados + resumo + tabela ----

    y = _desenhar_cabecalho(pdf, "Relatório de Vendas")
    y = _desenhar_metadados(
        pdf,
        y,
        [
            ("PERÍODO", f"{data_inicial_formatada} até {data_final_formatada}"),
            ("FILTRO", filtro_label),
        ]
    )
    y = _desenhar_resumo(pdf, y, resumo, tipo_vendas)
    y = _desenhar_titulo_secao(pdf, y, "Detalhamento")
    y = _desenhar_cabecalho_tabela(pdf, y)

    if not vendas:

        _desenhar_estado_vazio(pdf, y - 6)

    else:

        pagina_atual = _desenhar_tabela(
            pdf, y, vendas, COLUNAS_VENDAS, _celulas_vendas,
            "Relatório de Vendas", pagina_atual, total_paginas,
            data_geracao, _desenhar_cabecalho_tabela
        )

    _desenhar_rodape(pdf, pagina_atual, total_paginas, data_geracao)

    return pagina_atual


def gerar_relatorio_vendas_pdf(
    caminho_pdf,
    data_inicial,
    data_final,
    tipo_vendas,
    resumo,
    vendas
):

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

    argumentos = (
        data_geracao,
        data_inicial_formatada,
        data_final_formatada,
        filtro_label,
        tipo_vendas,
        resumo,
        vendas,
    )

    # Passada de medicao (em memoria): descobre o numero real de paginas,
    # ja considerando nomes que ocupam varias linhas, para "Pagina X de Y".
    medicao = canvas.Canvas(io.BytesIO(), pagesize=A4)
    total_paginas = _montar_relatorio_vendas(medicao, 0, *argumentos)

    pdf = canvas.Canvas(caminho_pdf, pagesize=A4)
    pdf.setTitle("Relatório de Vendas")

    _montar_relatorio_vendas(pdf, total_paginas, *argumentos)

    pdf.save()


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
        ("TICKET MÉDIO", moeda(resumo["ticket_medio"]), "neutro"),
    ]


def _desenhar_resumo_fechamento(pdf, y, resumo):

    y = _desenhar_titulo_secao(pdf, y, "Resumo do Dia")
    indicadores = _montar_indicadores_fechamento(resumo)

    return _desenhar_grade_indicadores(pdf, y, indicadores)


def _desenhar_cabecalho_tabela_fechamento(pdf, y):
    """Cabecalho da tabela do fechamento diario (6 colunas)."""

    return _desenhar_cabecalho_tabela(pdf, y, COLUNAS_FECHAMENTO)


def _celulas_fechamento(venda):
    """
    Mesmos campos de antes: hora, cliente, valor_total, valor_recebido,
    troco (cor de alerta quando negativo) e status_pagamento.
    """

    troco_valor = float(venda["troco"])

    return [
        ("texto", venda["data_venda"].strftime("%H:%M"), None),
        ("cliente", None, None),
        ("numero", moeda(venda["valor_total"]), COR_TEXTO),
        ("numero", moeda(venda["valor_recebido"]), COR_TEXTO),
        ("numero", moeda(venda["troco"]),
         COR_ALERTA if troco_valor < 0 else COR_TEXTO),
        ("status", venda["status_pagamento"], None),
    ]



def _montar_fechamento_diario(
    pdf, total_paginas, data_geracao, data_formatada, resumo, vendas
):
    """Desenha o documento inteiro e devolve o numero de paginas usadas."""

    pagina_atual = 1

    # ---- Primeira pagina: cabecalho + data + resumo + tabela ----

    y = _desenhar_cabecalho(pdf, "Fechamento Diário")
    y = _desenhar_metadados(pdf, y, [("DATA", data_formatada)])
    y = _desenhar_resumo_fechamento(pdf, y, resumo)
    y = _desenhar_titulo_secao(pdf, y, "Detalhamento")
    y = _desenhar_cabecalho_tabela_fechamento(pdf, y)

    if not vendas:

        _desenhar_estado_vazio(
            pdf,
            y - 6,
            "Nenhuma venda registrada",
            "para a data selecionada"
        )

    else:

        pagina_atual = _desenhar_tabela(
            pdf, y, vendas, COLUNAS_FECHAMENTO, _celulas_fechamento,
            "Fechamento Diário", pagina_atual, total_paginas,
            data_geracao, _desenhar_cabecalho_tabela_fechamento
        )

    _desenhar_rodape(pdf, pagina_atual, total_paginas, data_geracao)

    return pagina_atual


def gerar_fechamento_diario_pdf(
    caminho_pdf,
    data,
    resumo,
    vendas
):

    data_formatada = datetime.strptime(
        data, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    data_geracao = datetime.now()

    # Passada de medicao (em memoria) para o total real de paginas.
    medicao = canvas.Canvas(io.BytesIO(), pagesize=A4)
    total_paginas = _montar_fechamento_diario(
        medicao, 0, data_geracao, data_formatada, resumo, vendas
    )

    pdf = canvas.Canvas(caminho_pdf, pagesize=A4)
    pdf.setTitle("Fechamento Diário")

    _montar_fechamento_diario(
        pdf, total_paginas, data_geracao, data_formatada, resumo, vendas
    )

    pdf.save()


# ============================================================
# DESEMPENHO DE FUNCIONARIOS
# ============================================================
# Mesmo padrao dos outros relatorios: cabecalho, metadados,
# grade de indicadores, tabela com quebra de pagina e rodape.
# Os dados chegam prontos (resumo e funcionarios); aqui so ha
# apresentacao.

def _montar_indicadores_desempenho(resumo):

    return [
        ("FUNCIONÁRIOS", str(resumo["funcionarios"]), "neutro"),
        ("QUANTIDADE DE VENDAS", str(resumo["total_vendas"]), "neutro"),
        ("TOTAL VENDIDO", moeda(resumo["total_vendido"]), "neutro"),
        ("TICKET MÉDIO", moeda(resumo["ticket_medio"]), "neutro"),
    ]


def _desenhar_cabecalho_tabela_desempenho(pdf, y):

    return _desenhar_cabecalho_tabela(pdf, y, COLUNAS_DESEMPENHO)


def _celulas_desempenho(funcionario):

    return [
        ("cliente", None, None),
        ("numero", str(funcionario["quantidade_vendas"]), COR_TEXTO),
        ("numero", moeda(funcionario["total_vendido"]), COR_TEXTO),
        ("numero", moeda(funcionario["ticket_medio"]), COR_TEXTO),
    ]


def _montar_desempenho_funcionarios(
    pdf, total_paginas, data_geracao,
    data_inicial_formatada, data_final_formatada, resumo, funcionarios
):
    """Desenha o documento inteiro e devolve o numero de paginas usadas."""

    pagina_atual = 1

    y = _desenhar_cabecalho(pdf, "Desempenho de Funcionários")
    y = _desenhar_metadados(
        pdf,
        y,
        [("PERÍODO", f"{data_inicial_formatada} até {data_final_formatada}")]
    )

    y = _desenhar_titulo_secao(pdf, y, "Resumo")
    y = _desenhar_grade_indicadores(
        pdf, y, _montar_indicadores_desempenho(resumo)
    )

    y = _desenhar_titulo_secao(pdf, y, "Detalhamento por Funcionário")
    y = _desenhar_cabecalho_tabela_desempenho(pdf, y)

    if not funcionarios:

        _desenhar_estado_vazio(
            pdf,
            y - 6,
            "Nenhuma venda registrada",
            "no período selecionado"
        )

    else:

        pagina_atual = _desenhar_tabela(
            pdf, y, funcionarios, COLUNAS_DESEMPENHO, _celulas_desempenho,
            "Desempenho de Funcionários", pagina_atual, total_paginas,
            data_geracao, _desenhar_cabecalho_tabela_desempenho
        )

    _desenhar_rodape(pdf, pagina_atual, total_paginas, data_geracao)

    return pagina_atual


def gerar_desempenho_funcionarios_pdf(
    caminho_pdf,
    data_inicial,
    data_final,
    resumo,
    funcionarios
):

    data_inicial_formatada = datetime.strptime(
        data_inicial, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    data_final_formatada = datetime.strptime(
        data_final, "%Y-%m-%d"
    ).strftime("%d/%m/%Y")

    data_geracao = datetime.now()

    argumentos = (
        data_geracao,
        data_inicial_formatada,
        data_final_formatada,
        resumo,
        funcionarios,
    )

    # Passada de medicao (em memoria) para o total real de paginas.
    medicao = canvas.Canvas(io.BytesIO(), pagesize=A4)
    total_paginas = _montar_desempenho_funcionarios(
        medicao, 0, *argumentos
    )

    pdf = canvas.Canvas(caminho_pdf, pagesize=A4)
    pdf.setTitle("Desempenho de Funcionários")

    _montar_desempenho_funcionarios(pdf, total_paginas, *argumentos)

    pdf.save()