
# ============================================================
# MODEL DE FORNECEDOR
# ============================================================
# Este arquivo contém as funções responsáveis pelo acesso
# aos dados dos fornecedores no banco PostgreSQL.
#
# Funcionalidades:
# - Listar fornecedores ativos.
# - Cadastrar novos fornecedores.
# - Buscar um fornecedor pelo identificador.
# - Editar os dados de um fornecedor.
# - Desativar fornecedores.
# - Reativar fornecedores.
# - Listar fornecedores inativos.
#
# Este arquivo é responsável pelas consultas e alterações
# no banco de dados. O controle das requisições deve ficar
# nas rotas e nos controllers.
# ============================================================


# Importa a função que estabelece a conexão com o banco.
from app.database.conexao import conectar

# Permite retornar os resultados como dicionários, facilitando
# o acesso às informações pelo nome de cada coluna.
from psycopg2.extras import RealDictCursor


# ============================================================
# LISTAR FORNECEDORES ATIVOS
# ============================================================

def listar_fornecedores():
    """
    Lista os fornecedores que estão ativos.

    Retorno:
        Lista de dicionários com os dados dos fornecedores,
        ordenados alfabeticamente pelo nome.
    """

    # Abre uma conexão com o banco de dados.
    conexao = conectar()

    # Cria um cursor que retorna cada registro como dicionário.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Busca os fornecedores ativos.
    #
    # O filtro ativo = 1 mantém o comportamento original:
    # somente os fornecedores ativos são exibidos.
    #
    # A ordenação pelo nome facilita a localização na interface.
    sql = """
        SELECT *
        FROM fornecedor
        WHERE ativo = 1
        ORDER BY nome
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todos os fornecedores encontrados.
    fornecedores = cursor.fetchall()

    # Fecha o cursor e a conexão após a consulta.
    cursor.close()
    conexao.close()

    # Retorna os fornecedores para a camada responsável pela
    # apresentação dos dados.
    return fornecedores


# ============================================================
# CADASTRAR FORNECEDOR
# ============================================================

def cadastrar_fornecedor(
    nome,
    telefone,
    observacao
):
    """
    Cadastra um novo fornecedor no banco de dados.

    Parâmetros:
        nome: nome do fornecedor.
        telefone: telefone de contato.
        observacao: informações adicionais sobre o fornecedor.

    O banco recebe os dados informados e gera o identificador
    do fornecedor conforme a configuração da tabela.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar o INSERT.
    cursor = conexao.cursor()

    # Insere os dados básicos do fornecedor.
    #
    # Os valores são enviados separadamente da instrução SQL,
    # utilizando parâmetros do PostgreSQL.
    sql = """
        INSERT INTO fornecedor (
            nome,
            telefone,
            observacao
        )
        VALUES (%s, %s, %s)
    """

    # Executa a inserção com os dados recebidos.
    cursor.execute(
        sql,
        (
            nome,
            telefone,
            observacao
        )
    )

    # Confirma a gravação dos dados.
    conexao.commit()

    # Libera os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# BUSCAR FORNECEDOR POR ID
# ============================================================

def buscar_fornecedor_por_id(id_fornecedor):
    """
    Busca um fornecedor pelo seu identificador.

    Parâmetros:
        id_fornecedor: identificador do fornecedor.

    Retorno:
        Dicionário com os dados do fornecedor encontrado,
        ou None se não existir um registro correspondente.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Utiliza um cursor de dicionários para facilitar o acesso
    # aos campos retornados pela consulta.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Busca todas as colunas do fornecedor cujo identificador
    # corresponde ao valor recebido.
    sql = """
        SELECT *
        FROM fornecedor
        WHERE id = %s
    """

    # Executa a consulta usando o identificador informado.
    cursor.execute(
        sql,
        (id_fornecedor,)
    )

    # Recupera somente um registro.
    fornecedor = cursor.fetchone()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna o fornecedor encontrado ou None.
    return fornecedor


# ============================================================
# EDITAR FORNECEDOR
# ============================================================

def editar_fornecedor(
    id_fornecedor,
    nome,
    telefone,
    observacao
):
    """
    Atualiza os dados de um fornecedor existente.

    Parâmetros:
        id_fornecedor: identificador do fornecedor a editar.
        nome: novo nome do fornecedor.
        telefone: novo telefone de contato.
        observacao: nova observação.

    A atualização modifica os campos informados na consulta
    para o fornecedor que possui o identificador recebido.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Atualiza os dados cadastrais do fornecedor.
    #
    # O identificador é utilizado no WHERE para determinar
    # qual registro deve ser alterado.
    sql = """
        UPDATE fornecedor
        SET
            nome = %s,
            telefone = %s,
            observacao = %s
        WHERE id = %s
    """

    # Executa a atualização com os novos valores.
    cursor.execute(
        sql,
        (
            nome,
            telefone,
            observacao,
            id_fornecedor
        )
    )

    # Confirma as alterações no banco.
    conexao.commit()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()


# ============================================================
# DESATIVAR FORNECEDOR
# ============================================================

def desativar_fornecedor(fornecedor_id):
    """
    Desativa um fornecedor sem excluir seu registro.

    Parâmetro:
        fornecedor_id: identificador do fornecedor.

    A função altera o campo ativo para zero. O registro
    permanece no banco de dados, permitindo que seu histórico
    seja preservado.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Marca o fornecedor como inativo.
    #
    # A condição WHERE garante que somente o fornecedor
    # identificado pelo parâmetro seja alterado.
    sql = """
        UPDATE fornecedor
        SET ativo = 0
        WHERE id = %s
    """

    # Executa a desativação.
    cursor.execute(
        sql,
        (fornecedor_id,)
    )

    # Confirma a alteração no banco.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# REATIVAR FORNECEDOR
# ============================================================

def reativar_fornecedor(fornecedor_id):
    """
    Reativa um fornecedor anteriormente desativado.

    Parâmetro:
        fornecedor_id: identificador do fornecedor.

    A função altera o campo ativo para um, mantendo os demais
    dados cadastrais sem modificações.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor para executar o UPDATE.
    cursor = conexao.cursor()

    # Marca o fornecedor como ativo.
    sql = """
        UPDATE fornecedor
        SET ativo = 1
        WHERE id = %s
    """

    # Executa a reativação do fornecedor informado.
    cursor.execute(
        sql,
        (fornecedor_id,)
    )

    # Confirma a alteração.
    conexao.commit()

    # Fecha os recursos utilizados.
    cursor.close()
    conexao.close()


# ============================================================
# LISTAR FORNECEDORES INATIVOS
# ============================================================

def listar_fornecedores_inativos():
    """
    Lista os fornecedores que estão inativos.

    Retorno:
        Lista de dicionários com os dados dos fornecedores
        inativos, ordenados alfabeticamente pelo nome.
    """

    # Abre uma conexão com o banco.
    conexao = conectar()

    # Cria um cursor que retorna os registros como dicionários.
    cursor = conexao.cursor(cursor_factory=RealDictCursor)

    # Busca os fornecedores cujo campo ativo seja zero.
    #
    # A ordenação pelo nome mantém uma apresentação organizada
    # na interface de fornecedores inativos.
    sql = """
        SELECT *
        FROM fornecedor
        WHERE ativo = 0
        ORDER BY nome
    """

    # Executa a consulta.
    cursor.execute(sql)

    # Recupera todos os fornecedores inativos.
    dados = cursor.fetchall()

    # Fecha o cursor e a conexão.
    cursor.close()
    conexao.close()

    # Retorna os dados encontrados.
    return dados
