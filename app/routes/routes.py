# Importa jsonify para mostrar JSON no navegador
from flask import jsonify

# Importa controller
from controllers.cliente_controller import listar_clientes_controller


# Função responsável por configurar as rotas
def configurar_rotas(app):

    # Página inicial
    @app.route("/")
    def home():

        # Mensagem simples para testar Flask
        return "Sistema do TCC funcionando!"



    # Rota para testar conexão com banco
    @app.route("/clientes")
    def clientes():

        # Busca clientes pelo controller
        dados = listar_clientes_controller()

        # Converte para JSON
        return jsonify(dados)