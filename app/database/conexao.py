# Importa biblioteca que permite Python conversar com MySQL
import mysql.connector


# Função responsável por conectar no banco
def conectar():

    # Cria e retorna a conexão com o banco de dados
    return mysql.connector.connect(

        # Endereço do banco (localhost = seu computador)
        host="localhost",

        # Usuário padrão do XAMPP/MySQL
        user="root",

        # Senha do MySQL
        # No XAMPP normalmente fica vazio
        password="",

        # Nome do banco criado no phpMyAdmin
        database="tcc"
    )