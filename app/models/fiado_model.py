
# ============================================================
# MODEL DE FIADO
# ============================================================
# Este arquivo contém as funções responsáveis por consultar
# e atualizar as contas de fiado dos clientes.
#
# As funções deste model permitem:
# - Listar contas de fiado abertas.
# - Consultar os produtos vendidos em cada conta.
# - Buscar os dados de uma conta específica.
# - Atualizar o saldo devedor e o status da conta.
# - Registrar os pagamentos recebidos.
# - Consultar o histórico de recebimentos.
# - Buscar a conta aberta de um cliente.
# - Consultar as fichas de sinuca vinculadas ao fiado.
#
# O model é responsável pelo acesso ao banco de dados.
# A lógica de apresentação das informações deve ficar nos
# templates, enquanto o controle das requisições fica nas
# rotas e nos controllers.
# ============================================================


# Importa a função que estabelece a conexão com o PostgreSQL.
from app.database.conexao import conectar

# Permite retornar resultados das consultas como dicionários.
# Isso possibilita acessar os valores pelo nome das colunas,
# por exemplo: conta["saldo_devedor"].
from psycopg2.extras import RealDictCursor


# ============================================================
# LISTAR FIADOS
# ============================================================

def listar_fiados():
    """
    Lista todas as contas de fiado que estão abertas.

    A consulta retorna:
    - Identificador da conta.
    - Nome do cliente.
    - Saldo devedor.
    - Status da conta.
    - Data de abertura.

    Os registros são apresentados do mais recente para o
    mais antigo.

    Retorno:
        Lista de dicionários com os dados das contas abertas.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna os registros como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta as contas e relaciona cada uma ao cliente
    # correspondente por meio do identificador do cliente.
    #
    # O INNER JOIN faz com que sejam retornadas apenas as
    # contas que possuem um cliente correspondente.
    #
    # O filtro status_conta = 'aberta' limita os resultados
    # às contas que ainda estão abertas.
    sql = """
        SELECT
            conta.id,
            cliente.nome,
            conta.saldo_devedor,
            conta.status_conta,
            conta.data_abertura

        FROM conta

        INNER JOIN cliente
            ON cliente.id = conta.cliente_id

        WHERE conta.status_conta = 'aberta'

        ORDER BY conta.id DESC
    """

    # Executa a consulta SQL.
    cursor.execute(sql)

    # Recupera todas as contas encontradas.
    fiados = cursor.fetchall()

    # Fecha o cursor após concluir a consulta.
    cursor.close()

    # Fecha a conexão com o banco de dados.
    conexao.close()

    # Retorna a lista de contas para o controller ou a rota.
    return fiados


# ============================================================
# BUSCAR PRODUTOS DO FIADO
# ============================================================

def buscar_produtos_fiado(conta_id):
    """
    Busca os produtos das vendas vinculadas a uma conta de fiado.

    Parâmetro:
        conta_id: identificador da conta de fiado.

    Retorno:
        Lista de produtos com nome, quantidade, tipo de venda
        e identificador da venda relacionada.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Utiliza um cursor de dicionários para facilitar o acesso
    # às informações retornadas pela consulta.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Relaciona as vendas aos produtos vendidos.
    #
    # A tabela venda contém a conta à qual cada venda está
    # vinculada.
    #
    # A tabela produto_venda contém os produtos, as quantidades
    # e os tipos de venda registrados em cada venda.
    #
    # A tabela produto fornece o nome de cada produto.
    sql = """
        SELECT
            produto.nome,
            produto_venda.quantidade,
            produto_venda.tipo_venda,
            venda.id AS venda_id

        FROM venda

        INNER JOIN produto_venda
            ON venda.id = produto_venda.venda_id

        INNER JOIN produto
            ON produto.id = produto_venda.produto_id

        WHERE venda.conta_id = %s
    """

    # Executa a consulta para a conta informada.
    # O parâmetro é enviado separadamente da instrução SQL.
    cursor.execute(sql, (conta_id,))

    # Recupera todos os produtos encontrados.
    produtos = cursor.fetchall()

    # Libera os recursos utilizados na consulta.
    cursor.close()
    conexao.close()

    # Devolve a lista de produtos encontrados.
    return produtos


# ============================================================
# BUSCAR FIADO POR ID
# ============================================================

def buscar_fiado_por_id(conta_id):
    """
    Busca os dados de uma conta de fiado específica.

    Parâmetro:
        conta_id: identificador da conta que será consultada.

    Retorno:
        Dicionário com os campos da conta e o nome do cliente,
        ou None caso não seja encontrada uma conta correspondente.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna os resultados como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Seleciona todas as colunas da conta e acrescenta o nome
    # do cliente relacionado a ela.
    #
    # O INNER JOIN relaciona a conta ao cliente por cliente_id.
    # O filtro pelo identificador limita a busca a uma conta.
    sql = """
        SELECT
            conta.*,
            cliente.nome

        FROM conta

        INNER JOIN cliente
            ON cliente.id = conta.cliente_id

        WHERE conta.id = %s
    """

    # Executa a consulta para a conta solicitada.
    cursor.execute(sql, (conta_id,))

    # Como a consulta procura uma conta específica, recupera
    # somente um registro.
    fiado = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna a conta encontrada ou None.
    return fiado


# ============================================================
# ATUALIZAR SALDO DO FIADO
# ============================================================

def atualizar_saldo_fiado(
    conta_id,
    novo_saldo,
    status_conta
):
    """
    Atualiza o saldo devedor e o status de uma conta de fiado.

    Parâmetros:
        conta_id: identificador da conta que será atualizada.
        novo_saldo: novo valor do saldo devedor.
        status_conta: status que será gravado na conta.

    Esta função apenas atualiza os valores recebidos.
    O cálculo do novo saldo e a decisão sobre o status devem
    continuar sendo realizados pela camada responsável por
    controlar o fluxo do recebimento.
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Atualiza o saldo devedor e o status da conta identificada.
    #
    # Os três parâmetros são enviados separadamente:
    # 1. Novo saldo.
    # 2. Novo status.
    # 3. Identificador da conta que será atualizada.
    sql = """
        UPDATE conta

        SET
            saldo_devedor = %s,
            status_conta = %s

        WHERE id = %s
    """

    # Executa a atualização com os valores recebidos.
    cursor.execute(
        sql,
        (
            novo_saldo,
            status_conta,
            conta_id
        )
    )

    # Confirma a alteração no banco de dados.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

# ============================================================
# REGISTRAR RECEBIMENTO DO FIADO
# ============================================================

def registrar_recebimento_fiado(
    conta_id,
    valor_recebido
):
    """
    Registra um pagamento recebido de uma conta de fiado.

    Parâmetros:
        conta_id: identificador da conta que recebeu o pagamento.
        valor_recebido: valor do pagamento registrado.

    Esta função insere um registro no histórico de recebimentos.
    Ela não atualiza o saldo da conta; essa responsabilidade
    permanece na função atualizar_saldo_fiado().
    """

    # Abre a conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor para executar o INSERT.
    cursor = conexao.cursor()

    # Insere o recebimento na tabela de histórico.
    #
    # A data do recebimento não é informada explicitamente
    # nesta consulta. Portanto, o preenchimento desse campo
    # depende da configuração existente na tabela do banco.
    sql = """
        INSERT INTO recebimento_fiado (
            conta_id,
            valor_recebido
        )

        VALUES (%s, %s)
    """

    # Registra o identificador da conta e o valor recebido.
    cursor.execute(
        sql,
        (
            conta_id,
            valor_recebido
        )
    )

    # Confirma a gravação do recebimento.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# BUSCAR RECEBIMENTOS DO FIADO
# ============================================================

def buscar_recebimentos_fiado(conta_id):
    """
    Busca o histórico de pagamentos de uma conta de fiado.

    Parâmetro:
        conta_id: identificador da conta consultada.

    Retorno:
        Lista de dicionários contendo o valor recebido e a
        data de cada recebimento, do mais recente para o mais antigo.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Utiliza um cursor de dicionários para permitir o acesso
    # aos resultados pelo nome das colunas.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta os recebimentos vinculados à conta.
    #
    # A ordenação decrescente pela data coloca os registros
    # mais recentes no início da lista.
    sql = """
        SELECT
            valor_recebido,
            data_recebimento

        FROM recebimento_fiado

        WHERE conta_id = %s

        ORDER BY data_recebimento DESC
    """

    # Executa a consulta para a conta informada.
    cursor.execute(sql, (conta_id,))

    # Recupera todos os recebimentos encontrados.
    recebimentos = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna o histórico de recebimentos.
    return recebimentos


# ============================================================
# BUSCAR CONTA ABERTA POR CLIENTE
# ============================================================

def buscar_conta_por_cliente(cliente_id):
    """
    Busca uma conta de fiado aberta vinculada a um cliente.

    Parâmetro:
        cliente_id: identificador do cliente.

    Retorno:
        Dicionário contendo o identificador da conta encontrada,
        ou None quando não existir uma conta aberta correspondente.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna o resultado como dicionário.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Procura uma conta do cliente cujo status seja 'aberta'.
    #
    # O LIMIT 1 faz com que a consulta retorne, no máximo,
    # um registro.
    sql = """
        SELECT id

        FROM conta

        WHERE cliente_id = %s

        AND status_conta = 'aberta'

        LIMIT 1
    """

    # Executa a consulta para o cliente informado.
    cursor.execute(sql, (cliente_id,))

    # Recupera a conta encontrada, se houver.
    conta = cursor.fetchone()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()

    # Retorna o resultado da busca.
    return conta


# ============================================================
# BUSCAR FICHAS DE SINUCA DO FIADO
# ============================================================

def buscar_fichas_fiado(conta_id):
    """
    Busca as fichas de sinuca relacionadas às vendas de uma
    conta de fiado.

    Parâmetro:
        conta_id: identificador da conta de fiado.

    Retorno:
        Lista de registros contendo a quantidade de fichas,
        o valor unitário e o valor total.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Utiliza um cursor de dicionários para acessar os valores
    # retornados pelo nome das colunas.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Consulta as fichas de sinuca associadas às vendas
    # vinculadas à conta de fiado.
    #
    # A tabela sinuca_venda contém os dados das fichas.
    # A tabela venda permite localizar a conta relacionada
    # a cada registro de fichas.
    sql = """
        SELECT
            sv.quantidade_fichas,
            sv.valor_unitario,
            sv.valor_total

        FROM sinuca_venda sv

        INNER JOIN venda v
            ON sv.venda_id = v.id

        WHERE v.conta_id = %s
    """

    # Executa a consulta para a conta informada.
    cursor.execute(sql, (conta_id,))

    # Recupera todos os registros de fichas encontrados.
    fichas = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna a lista de fichas relacionadas à conta.
    return fichas
