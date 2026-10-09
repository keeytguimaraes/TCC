# ==================================================
# IMPORTAÇÕES
# ==================================================

# Biblioteca utilizada para acessar
# variáveis de ambiente do sistema.
import os

# Biblioteca responsável pela conexão
# com o PostgreSQL.
import psycopg2

# Biblioteca utilizada para carregar
# automaticamente as variáveis definidas
# no arquivo .env.
from dotenv import load_dotenv


# ==================================================
# CARREGA VARIÁVEIS DE AMBIENTE
# ==================================================
#
# Ao iniciar a aplicação, o Python irá
# ler o arquivo .env e disponibilizar
# suas variáveis através do os.getenv().
#
# Exemplo:
#
# DATABASE_URL=postgresql://...
#
# ==================================================

load_dotenv()


# ==================================================
# CRIAR CONEXÃO COM O BANCO
# ==================================================
#
# Esta função é utilizada por todos
# os models do sistema.
#
# Sua responsabilidade é criar e
# retornar uma conexão ativa com
# o banco de dados PostgreSQL.
#
# A URL de conexão é obtida através
# da variável de ambiente DATABASE_URL.
#
# Exemplo de uso:
#
# conexao = conectar()
#
# cursor = conexao.cursor()
#
# ==================================================

def conectar():

    return psycopg2.connect(

        os.getenv(
            "DATABASE_URL"
        )
    )