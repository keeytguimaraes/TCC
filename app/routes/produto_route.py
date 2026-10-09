
# ============================================================
# ROTAS DE PRODUTOS — SIGC
# ============================================================
# Este arquivo concentra as rotas relacionadas ao cadastro
# e ao gerenciamento de produtos.
#
# Funcionalidades:
# - Listar todos os produtos;
# - Listar produtos ativos;
# - Listar produtos inativos;
# - Cadastrar produtos;
# - Editar e atualizar produtos;
# - Inativar e reativar produtos;
# - Consultar detalhes e histórico de preços.
#
# As regras de negócio e as operações no banco de dados
# permanecem nos controllers e models.
# ============================================================


# Importa os decorators responsáveis pelo controle de acesso.
from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)

# Importa as ferramentas utilizadas nas rotas Flask.
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa as funções do controller de produtos.
from app.controllers.produto_controller import (
    pegar_produtos,
    pegar_produtos_ativos,
    pegar_produtos_inativos,
    cadastrar_produto_controller,
    pegar_produto_por_id,
    editar_produto_controller,
    inativar_produto_controller,
    ativar_produto_controller,
    pegar_historico_preco
)

# secure_filename prepara o nome do arquivo enviado
# para ser utilizado como nome de arquivo no servidor.
from werkzeug.utils import secure_filename

# os permite construir caminhos de arquivos de forma
# compatível com o sistema operacional.
import os


# ============================================================
# CONFIGURAÇÃO DAS ROTAS DE PRODUTOS
# ============================================================
def configurar_produto_routes(app):
    """
    Registra todas as rotas relacionadas aos produtos.

    Parâmetros:
        app: instância principal da aplicação Flask.
    """

    # --------------------------------------------------------
    # LISTAR TODOS OS PRODUTOS
    # --------------------------------------------------------
    # URL: /produto
    # Método: GET
    #
    # Exibe a listagem geral de produtos.
    # O acesso exige autenticação e perfil de administrador
    # ou gerente, conforme os decorators já existentes.
    @app.route("/produto")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador",
        "gerente"
    )
    def produto():
        """
        Busca todos os produtos e apresenta a listagem.
        """

        # Solicita ao controller os dados dos produtos.
        dados = pegar_produtos()

        # Abre o template da listagem e envia os dados
        # usando a variável 'produtos'.
        return render_template(
            "produto/produto.html",
            produtos=dados
        )

    # --------------------------------------------------------
    # LISTAR PRODUTOS ATIVOS
    # --------------------------------------------------------
    # URL: /produto/ativos
    # Método: GET
    #
    # Exibe somente os produtos ativos.
    @app.route("/produto/ativos")
    def produtos_ativos():
        """
        Busca os produtos ativos e apresenta a listagem.
        """

        # Busca a lista de produtos ativos no controller.
        dados = pegar_produtos_ativos()

        # Reutiliza o mesmo template da listagem geral.
        return render_template(
            "produto/produto.html",
            produtos=dados
        )

    # --------------------------------------------------------
    # LISTAR PRODUTOS INATIVOS
    # --------------------------------------------------------
    # URL: /produto/inativos
    # Método: GET
    #
    # Exibe somente os produtos inativos.
    @app.route("/produto/inativos")
    def produtos_inativos():
        """
        Busca os produtos inativos e apresenta a listagem.
        """

        # Busca a lista de produtos inativos no controller.
        dados = pegar_produtos_inativos()

        # Reutiliza o template geral de produtos.
        return render_template(
            "produto/produto.html",
            produtos=dados
        )

    # --------------------------------------------------------
    # CADASTRAR PRODUTO
    # --------------------------------------------------------
    # URL: /produto/cadastrar
    # Método: POST
    #
    # Recebe os dados enviados pelo formulário de cadastro,
    # prepara os valores e chama o controller responsável
    # por cadastrar o produto.
    @app.route(
        "/produto/cadastrar",
        methods=["POST"]
    )
    def cadastrar_produto():
        """
        Recebe os dados do formulário e cadastra um produto.
        """

        # ----------------------------------------------------
        # 1. DADOS BÁSICOS DO PRODUTO
        # ----------------------------------------------------
        # request.form.get() recupera o valor de um campo
        # enviado pelo formulário HTML.
        #
        # Se o campo não existir, o resultado será None.
        nome = request.form.get(
            "nome"
        )

        categoria = request.form.get(
            "categoria"
        )

        sabor = request.form.get(
            "sabor"
        )

        tipo_embalagem = request.form.get(
            "tipo_embalagem"
        )

        # ----------------------------------------------------
        # 2. VOLUME OU PESO DO PRODUTO
        # ----------------------------------------------------
        # O valor numérico é convertido para float para
        # permitir valores decimais, como 1.5 litro.
        #
        # Se o campo não existir, utiliza-se zero.
        # Observação: um campo vazio pode gerar ValueError
        # nesta conversão, mantendo o comportamento original.
        valor_volume = float(
            request.form.get(
                "valor_volume",
                0
            )
        )

        # Guarda a unidade selecionada no formulário.
        # Exemplos possíveis: L, kg ou outra unidade usada
        # pela interface do sistema.
        unidade_volume = request.form.get(
            "unidade_volume"
        )

        # Monta o texto do volume com o valor e a unidade.
        # Exemplo: valor_volume = 2 e unidade_volume = "L"
        # resulta no texto "2.0L".
        volume = (
            str(valor_volume)
            + unidade_volume
        )

        # ----------------------------------------------------
        # 3. CONVERTER O VOLUME PARA A UNIDADE BASE
        # ----------------------------------------------------
        # Para litros e quilogramas, o código multiplica
        # o valor por 1000.
        #
        # Para outras unidades, conserva o valor numérico.
        #
        # Essa variável é enviada ao controller para que
        # o processamento do produto utilize o valor base.
        if unidade_volume == "L":

            # Converte litros para mililitros.
            quantidade_por_unidade = (
                valor_volume * 1000
            )

        elif unidade_volume == "kg":

            # Converte quilogramas para gramas.
            quantidade_por_unidade = (
                valor_volume * 1000
            )

        else:

            # Para outras unidades, mantém o valor original.
            quantidade_por_unidade = (
                valor_volume
            )

        # ----------------------------------------------------
        # 4. PREÇOS DO PRODUTO
        # ----------------------------------------------------
        # Os valores são obtidos do formulário sem conversão
        # explícita, como no código original.
        # A interpretação e a validação desses valores ficam
        # a cargo das camadas responsáveis pelo processamento.
        preco_venda = request.form.get(
            "preco_venda"
        )

        preco_caixa = request.form.get(
            "preco_caixa"
        )

        preco_dose = request.form.get(
            "preco_dose"
        )

        preco_unidade = request.form.get(
            "preco_unidade"
        )

        # ----------------------------------------------------
        # 5. CONFIGURAÇÕES DE ESTOQUE
        # ----------------------------------------------------
        # quantidade_por_caixa informa quantas unidades
        # existem em cada caixa do produto.
        quantidade_por_caixa = request.form.get(
            "quantidade_por_caixa"
        )

        # Define a quantidade mínima usada pelo sistema
        # como referência para o estoque.
        estoque_minimo = request.form.get(
            "estoque_minimo"
        )

        # ----------------------------------------------------
        # 6. TIPOS DE VENDA PERMITIDOS
        # ----------------------------------------------------
        # Os campos de seleção, como checkboxes, normalmente
        # só aparecem em request.form quando estão marcados.
        #
        # Por isso, a verificação 'is not None' transforma
        # a presença do campo em um valor booleano.
        vende_por_dose = (
            request.form.get(
                "vende_por_dose"
            ) is not None
        )

        vende_por_unidade = (
            request.form.get(
                "vende_por_unidade"
            ) is not None
        )

        # Recupera o volume de cada dose, caso esse tipo
        # de venda esteja configurado para o produto.
        volume_dose_ml = request.form.get(
            "volume_dose_ml"
        )

        # ----------------------------------------------------
        # 7. IMAGEM DO PRODUTO
        # ----------------------------------------------------
        # Recupera o arquivo enviado pelo formulário.
        # Caso nenhuma imagem seja enviada, o valor poderá
        # ser None.
        imagem = request.files.get(
            "imagem"
        )

        # Inicialmente, considera que o produto não possui
        # um novo nome de imagem para salvar.
        nome_imagem = None

        # Só salva o arquivo se ele existir e possuir nome.
        if imagem and imagem.filename != "":

            # Prepara o nome do arquivo para evitar que
            # componentes de caminho enviados no nome sejam
            # tratados como parte do caminho de destino.
            nome_imagem = secure_filename(
                imagem.filename
            )

            # Monta o caminho de destino da imagem.
            # os.path.join combina a pasta com o nome do arquivo.
            caminho = os.path.join(
                "app/static/uploads/produtos",
                nome_imagem
            )

            # Salva a imagem no caminho especificado.
            imagem.save(
                caminho
            )

        # ----------------------------------------------------
        # 8. ENVIAR OS DADOS PARA O CONTROLLER
        # ----------------------------------------------------
        # A chamada preserva a ordem dos argumentos do código
        # original. O controller é responsável por encaminhar
        # os dados para o model e realizar o cadastro.
        cadastrar_produto_controller(
            nome,
            categoria,
            sabor,
            tipo_embalagem,
            volume,
            preco_venda,
            preco_caixa,
            quantidade_por_caixa,
            estoque_minimo,
            vende_por_dose,
            vende_por_unidade,
            volume_dose_ml,
            preco_dose,
            preco_unidade,
            quantidade_por_unidade,
            nome_imagem
        )

        # Informa à interface que o cadastro foi concluído.
        flash(
            "Produto cadastrado com sucesso!",
            "success"
        )

        # Retorna à listagem de produtos.
        return redirect(
            "/produto"
        )

    # --------------------------------------------------------
    # EXIBIR PÁGINA DE EDIÇÃO
    # --------------------------------------------------------
    # URL: /produto/editar/<produto_id>
    # Método: GET
    #
    # Recebe o ID do produto pela URL, busca os dados
    # correspondentes e os disponibiliza no formulário.
    @app.route(
        "/produto/editar/<int:produto_id>"
    )
    def editar_produto_page(produto_id):
        """
        Busca um produto e abre sua página de edição.
        """

        # Busca os dados do produto pelo identificador.
        produto = pegar_produto_por_id(
            produto_id
        )

        # Abre o formulário preenchido com os dados encontrados.
        return render_template(
            "produto/editar_produto.html",
            produto=produto
        )

    # --------------------------------------------------------
    # ATUALIZAR PRODUTO
    # --------------------------------------------------------
    # URL: /produto/atualizar/<produto_id>
    # Método: POST
    #
    # Recebe os valores editados e os envia ao controller.
    @app.route(
        "/produto/atualizar/<int:produto_id>",
        methods=["POST"]
    )
    def atualizar_produto(produto_id):
        """
        Atualiza os dados de um produto existente.
        """

        # ----------------------------------------------------
        # 1. RECUPERAR OS DADOS BÁSICOS
        # ----------------------------------------------------
        nome = request.form.get(
            "nome"
        )

        categoria = request.form.get(
            "categoria"
        )

        sabor = request.form.get(
            "sabor"
        )

        tipo_embalagem = request.form.get(
            "tipo_embalagem"
        )

        # Durante a edição, o volume é recebido diretamente
        # do campo chamado 'volume'.
        volume = request.form.get(
            "volume"
        )

        # ----------------------------------------------------
        # 2. RECUPERAR OS PREÇOS
        # ----------------------------------------------------
        preco_venda = request.form.get(
            "preco_venda"
        )

        preco_caixa = request.form.get(
            "preco_caixa"
        )

        preco_dose = request.form.get(
            "preco_dose"
        )

        preco_unidade = request.form.get(
            "preco_unidade"
        )

        # ----------------------------------------------------
        # 3. RECUPERAR AS CONFIGURAÇÕES DE ESTOQUE
        # ----------------------------------------------------
        quantidade_por_caixa = request.form.get(
            "quantidade_por_caixa"
        )

        # Recupera a quantidade correspondente a cada unidade.
        # Diferentemente do cadastro, aqui o valor vem
        # diretamente do formulário de edição.
        quantidade_por_unidade = request.form.get(
            "quantidade_por_unidade"
        )

        # ----------------------------------------------------
        # 4. RECUPERAR OS TIPOS DE VENDA
        # ----------------------------------------------------
        # Converte a presença dos campos em valores booleanos,
        # mantendo a mesma lógica utilizada no cadastro.
        vende_por_dose = (
            request.form.get(
                "vende_por_dose"
            ) is not None
        )

        vende_por_unidade = (
            request.form.get(
                "vende_por_unidade"
            ) is not None
        )

        # Recupera o volume de cada dose.
        volume_dose_ml = request.form.get(
            "volume_dose_ml"
        )

        # ----------------------------------------------------
        # 5. ENVIAR OS DADOS PARA O CONTROLLER
        # ----------------------------------------------------
        # Mantém a ordem original dos argumentos.
        # O ID identifica qual produto será atualizado.
        editar_produto_controller(
            produto_id,
            nome,
            categoria,
            sabor,
            tipo_embalagem,
            volume,
            preco_venda,
            preco_caixa,
            quantidade_por_caixa,
            vende_por_dose,
            vende_por_unidade,
            volume_dose_ml,
            preco_dose,
            preco_unidade,
            quantidade_por_unidade
        )

        # Exibe uma mensagem após a chamada ao controller
        # terminar sem lançar uma exceção.
        flash(
            "Produto atualizado com sucesso!",
            "success"
        )

        # Retorna à listagem de produtos.
        return redirect(
            "/produto"
        )

    # --------------------------------------------------------
    # INATIVAR PRODUTO
    # --------------------------------------------------------
    # URL: /produto/inativar/<produto_id>
    # Método: POST
    #
    # Encaminha o ID do produto ao controller para realizar
    # a inativação.
    @app.route(
        "/produto/inativar/<int:produto_id>",
        methods=["POST"]
    )
    def inativar_produto(produto_id):
        """
        Solicita a inativação de um produto.
        """

        # Executa a operação no controller.
        inativar_produto_controller(
            produto_id
        )

        # Informa que a operação foi concluída.
        flash(
            "Produto inativado com sucesso!",
            "success"
        )

        # Retorna à listagem geral.
        return redirect(
            "/produto"
        )

    # --------------------------------------------------------
    # ATIVAR PRODUTO
    # --------------------------------------------------------
    # URL: /produto/ativar/<produto_id>
    # Método: POST
    #
    # Encaminha o ID do produto ao controller para realizar
    # a ativação.
    @app.route(
        "/produto/ativar/<int:produto_id>",
        methods=["POST"]
    )
    def ativar_produto_route(produto_id):
        """
        Solicita a ativação de um produto.
        """

        # Executa a operação no controller.
        ativar_produto_controller(
            produto_id
        )

        # Informa que a operação foi concluída.
        flash(
            "Produto ativado com sucesso!",
            "success"
        )

        # Retorna à listagem geral.
        return redirect(
            "/produto"
        )

    # --------------------------------------------------------
    # DETALHES E HISTÓRICO DE PREÇOS DO PRODUTO
    # --------------------------------------------------------
    # URL: /produto/detalhes/<produto_id>
    # Método: GET
    #
    # Busca os dados do produto e seu histórico de preços
    # para apresentar ambos na mesma página.
    @app.route(
        "/produto/detalhes/<int:produto_id>"
    )
    def detalhes_produto_produto(produto_id):
        """
        Exibe os detalhes de um produto e seu histórico de preços.
        """

        # Busca as informações atuais do produto.
        produto = pegar_produto_por_id(
            produto_id
        )

        # Busca o histórico de preços associado ao produto.
        historico = pegar_historico_preco(
            produto_id
        )

        # Renderiza a página com as duas informações.
        return render_template(
            "produto/detalhes_produto.html",
            produto=produto,
            historico=historico
        )
