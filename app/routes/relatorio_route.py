
# ============================================================
# ROTAS DE RELATÓRIOS — SIGC
# ============================================================
# Este arquivo reúne as rotas responsáveis pela visualização
# e pela geração de relatórios em PDF.
#
# Funcionalidades:
# - Exibir o painel de relatórios;
# - Exibir a tela de relatório de vendas;
# - Gerar PDF das vendas de um período;
# - Exibir a tela de fechamento diário;
# - Gerar PDF do fechamento diário.
#
# As consultas dos dados são realizadas pelos controllers.
# A formatação dos documentos PDF é delegada às funções
# geradoras específicas.
# ============================================================


# Importa os decorators que controlam o acesso às rotas.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas necessárias do Flask.
from flask import (
    render_template,
    request,
    send_file
)

# Importa o controller responsável pelos dados gerais
# apresentados na página principal de relatórios.
from app.controllers.relatorio_controller import (
    pegar_relatorio
)

# Importa as funções responsáveis por consultar os dados
# dos relatórios de vendas e do fechamento diário.
from app.controllers.relatorio_pdf_controller import (
    pegar_vendas_periodo,
    pegar_resumo_periodo,
    pegar_fechamento_dia,
    pegar_resumo_fechamento
)

# Importa as funções que geram os arquivos PDF.
from app.utils.pdf_generator import (
    gerar_relatorio_vendas_pdf,
    gerar_fechamento_diario_pdf
)

# datetime permite obter a data e a hora atuais para
# identificar os arquivos gerados.
from datetime import datetime

# os permite criar diretórios e verificar caminhos
# relacionados ao sistema de arquivos.
import os


# ============================================================
# CONFIGURAR ROTAS DE RELATÓRIOS
# ============================================================
def configurar_relatorio_routes(app):
    """
    Registra as rotas relacionadas aos relatórios do SIGC.

    Parâmetros:
        app: instância principal da aplicação Flask.
    """

    # --------------------------------------------------------
    # PAINEL PRINCIPAL DE RELATÓRIOS
    # --------------------------------------------------------
    # URL: /relatorio
    # Método: GET
    #
    # Exige que o usuário esteja autenticado e tenha perfil
    # de administrador ou gerente.
    @app.route("/relatorio")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def relatorio():
        """
        Exibe a página principal de relatórios.
        """

        # Busca os dados necessários para preencher o painel.
        dados = pegar_relatorio()

        # Renderiza a página principal e disponibiliza
        # os dados por meio da variável 'dados'.
        return render_template(
            "relatorio/relatorio.html",
            dados=dados
        )

    # --------------------------------------------------------
    # TELA DO RELATÓRIO DE VENDAS
    # --------------------------------------------------------
    # URL: /relatorio/vendas
    # Método: GET
    #
    # Exibe o formulário utilizado para escolher o período
    # e o tipo de vendas que será incluído no PDF.
    @app.route("/relatorio/vendas")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def tela_relatorio_vendas():
        """
        Exibe o formulário de geração do relatório de vendas.
        """

        # Abre o template que contém o formulário do relatório.
        return render_template(
            "relatorio/vendas.html"
        )

    # --------------------------------------------------------
    # GERAR RELATÓRIO DE VENDAS EM PDF
    # --------------------------------------------------------
    # URL: /relatorio/vendas/pdf
    # Método: POST
    #
    # Recebe as informações do formulário, consulta as vendas
    # e o resumo do período, gera o PDF e envia o documento
    # como resposta da requisição.
    @app.route(
        "/relatorio/vendas/pdf",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def gerar_relatorio_vendas():
        """
        Gera um PDF com as vendas de um período selecionado.
        """

        # ----------------------------------------------------
        # 1. RECUPERAR OS FILTROS DO FORMULÁRIO
        # ----------------------------------------------------
        # Obtém a data inicial e a data final escolhidas.
        # Os valores são recebidos como strings pelo Flask.
        data_inicial = request.form.get(
            "data_inicial"
        )

        data_final = request.form.get(
            "data_final"
        )

        # Recupera o tipo de vendas selecionado.
        # A interpretação desse filtro é responsabilidade
        # do controller que consulta os dados.
        tipo_vendas = request.form.get(
            "tipo_vendas"
        )

        # ----------------------------------------------------
        # 2. BUSCAR AS VENDAS DO PERÍODO
        # ----------------------------------------------------
        # Consulta as vendas que correspondem às datas
        # e ao tipo de venda informado.
        vendas = pegar_vendas_periodo(
            data_inicial,
            data_final,
            tipo_vendas
        )

        # ----------------------------------------------------
        # 3. BUSCAR O RESUMO DO PERÍODO
        # ----------------------------------------------------
        # Obtém os dados resumidos que serão apresentados
        # no relatório, utilizando os mesmos filtros.
        resumo = pegar_resumo_periodo(
            data_inicial,
            data_final,
            tipo_vendas
        )

        # ----------------------------------------------------
        # 4. PREPARAR A PASTA DOS RELATÓRIOS
        # ----------------------------------------------------
        # Cria a pasta 'relatorios' caso ela ainda não exista.
        #
        # exist_ok=True impede que a operação gere um erro
        # simplesmente porque o diretório já existe.
        os.makedirs(
            "relatorios",
            exist_ok=True
        )

        # ----------------------------------------------------
        # 5. CRIAR UM IDENTIFICADOR PARA O ARQUIVO
        # ----------------------------------------------------
        # Obtém a data e a hora atuais no formato:
        # ano, mês, dia, hora, minuto e segundo.
        #
        # Exemplo: 20261009_143025
        #
        # Esse identificador é utilizado no nome do PDF.
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # Monta o caminho completo do arquivo que será gerado.
        caminho_pdf = (
            f"relatorios/relatorio_vendas_{timestamp}.pdf"
        )

        # ----------------------------------------------------
        # 6. GERAR O DOCUMENTO PDF
        # ----------------------------------------------------
        # Envia o caminho do arquivo, os filtros, o resumo
        # e a lista de vendas para a função responsável
        # por montar e salvar o relatório.
        gerar_relatorio_vendas_pdf(
            caminho_pdf,
            data_inicial,
            data_final,
            tipo_vendas,
            resumo,
            vendas
        )

        # ----------------------------------------------------
        # 7. ENVIAR O PDF AO NAVEGADOR
        # ----------------------------------------------------
        # send_file disponibiliza o arquivo como resposta.
        # O mimetype informa ao navegador que o conteúdo
        # enviado é um documento PDF.
        return send_file(
            caminho_pdf,
            mimetype="application/pdf"
        )

    # --------------------------------------------------------
    # TELA DE FECHAMENTO DIÁRIO
    # --------------------------------------------------------
    # URL: /relatorio/fechamento
    # Método: GET
    #
    # Exibe o formulário usado para selecionar a data
    # do fechamento diário.
    @app.route(
        "/relatorio/fechamento"
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def tela_fechamento_diario():
        """
        Exibe a página de fechamento diário.
        """

        # Abre o formulário de fechamento diário.
        return render_template(
            "relatorio/fechamento_diario.html"
        )

    # --------------------------------------------------------
    # GERAR FECHAMENTO DIÁRIO EM PDF
    # --------------------------------------------------------
    # URL: /relatorio/fechamento/pdf
    # Método: POST
    #
    # Recebe a data escolhida, consulta os dados do fechamento,
    # gera o documento PDF e o envia ao navegador.
    @app.route(
        "/relatorio/fechamento/pdf",
        methods=["POST"]
    )
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def gerar_fechamento_diario():
        """
        Gera o PDF do fechamento diário para uma data.
        """

        # ----------------------------------------------------
        # 1. RECUPERAR A DATA DO FORMULÁRIO
        # ----------------------------------------------------
        # Obtém a data para a qual o usuário solicitou
        # o fechamento diário.
        data = request.form.get(
            "data"
        )

        # ----------------------------------------------------
        # 2. BUSCAR OS DADOS DO FECHAMENTO
        # ----------------------------------------------------
        # Busca as vendas associadas à data selecionada.
        vendas = pegar_fechamento_dia(
            data
        )

        # Busca o resumo financeiro do fechamento.
        resumo = pegar_resumo_fechamento(
            data
        )

        # ----------------------------------------------------
        # 3. PREPARAR O NOME DO ARQUIVO
        # ----------------------------------------------------
        # Mantém a criação do identificador de data e hora
        # existente no código original.
        #
        # Essa variável é preservada para não remover uma
        # operação que já existia no arquivo, embora não seja
        # utilizada na montagem do caminho abaixo.
        data_arquivo = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # Monta o nome do PDF utilizando a data e a hora
        # atuais, evitando que arquivos gerados em momentos
        # diferentes tenham exatamente o mesmo nome,
        # desde que sejam gerados em segundos distintos.
        nome_arquivo = (
            f"fechamento_diario_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

        # Define o caminho em que o documento será salvo.
        caminho_pdf = (
            f"relatorios/{nome_arquivo}"
        )

        # ----------------------------------------------------
        # 4. GERAR O DOCUMENTO PDF
        # ----------------------------------------------------
        # Envia o caminho, a data selecionada, o resumo
        # e os dados das vendas para a função geradora.
        gerar_fechamento_diario_pdf(
            caminho_pdf,
            data,
            resumo,
            vendas
        )

        # ----------------------------------------------------
        # 5. ENVIAR O PDF AO NAVEGADOR
        # ----------------------------------------------------
        # Retorna o arquivo gerado ao navegador como PDF.
        return send_file(
            caminho_pdf,
            mimetype="application/pdf"
        )
