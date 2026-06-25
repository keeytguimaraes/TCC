# Importa Flask
from flask import Flask

# Importa rotas de cliente
from app.routes.cliente_route import configurar_cliente_routes
# Importa rota produto
from app.routes.produto_route import configurar_produto_routes
# Importa rota estoque
from app.routes.estoque_route import configurar_estoque_routes
# Importa rota fornecedor
from app.routes.fornecedor_route import configurar_fornecedor_routes
# Importa rota venda
from app.routes.venda_route import configurar_venda_routes
# Importa rota conta
from app.routes.conta_route import configurar_conta_routes
# Importa rota fiado
from app.routes.fiado_route import configurar_fiado_routes
# Importa rota relatório
from app.routes.relatorio_route import configurar_relatorio_routes

# Cria aplicação Flask
app = Flask(

    # Nome da aplicação
    __name__,

    # Diz onde estão os arquivos HTML
    template_folder="app/templates",

    # Diz onde ficarão CSS, JS e imagens futuramente
    static_folder="app/static"
)
# SECRET KEY
app.secret_key = "tcc_bar"


# Registra rotas
configurar_cliente_routes(app)
configurar_produto_routes(app)
configurar_estoque_routes(app)
configurar_fornecedor_routes(app)
configurar_venda_routes(app)
configurar_conta_routes(app)
configurar_fiado_routes(app)
configurar_relatorio_routes(app)

# Inicia servidor
if __name__ == "__main__":

    # debug=True atualiza automaticamente ao salvar
    app.run(debug=True)