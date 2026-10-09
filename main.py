
# ============================================================
# ARQUIVO PRINCIPAL DA APLICAÇÃO — SIGC
# ============================================================
# Este arquivo é responsável por inicializar a aplicação Flask
# e conectar os principais componentes do sistema.
#
# Responsabilidades:
# - Criar a aplicação Flask;
# - Configurar os diretórios de templates e arquivos estáticos;
# - Definir a chave utilizada para assinar a sessão;
# - Configurar o tratamento de erros HTTP;
# - Verificar globalmente se o usuário está autenticado;
# - Registrar as rotas de todos os módulos;
# - Iniciar o servidor quando o arquivo for executado diretamente.
# ============================================================


# ------------------------------------------------------------
# IMPORTAÇÕES DO FLASK
# ------------------------------------------------------------
# Flask: cria a aplicação web.
# render_template: renderiza arquivos HTML.
# session: acessa os dados da sessão do usuário.
# redirect: redireciona o navegador para outra rota.
# request: permite consultar informações da requisição atual.
from flask import (
    Flask,
    render_template,
    session,
    redirect,
    request
)


# ------------------------------------------------------------
# IMPORTAÇÕES DAS ROTAS
# ------------------------------------------------------------
# Cada função configurar_*_routes recebe a aplicação Flask
# e registra nela as rotas do módulo correspondente.

# Rotas de autenticação: login e logout.
from app.routes.auth_route import (
    configurar_auth_routes
)

# Rotas de clientes.
from app.routes.cliente_route import (
    configurar_cliente_routes
)

# Rotas de produtos.
from app.routes.produto_route import (
    configurar_produto_routes
)

# Rotas de estoque.
from app.routes.estoque_route import (
    configurar_estoque_routes
)

# Rotas de fornecedores.
from app.routes.fornecedor_route import (
    configurar_fornecedor_routes
)

# Rotas de vendas.
from app.routes.venda_route import (
    configurar_venda_routes
)

# Rotas do carrinho de compras.
from app.routes.carrinho_route import (
    configurar_carrinho_routes
)

# Rotas de contas pendentes.
from app.routes.conta_route import (
    configurar_conta_routes
)

# Rotas de vendas fiadas.
from app.routes.fiado_route import (
    configurar_fiado_routes
)

# Rotas de relatórios.
from app.routes.relatorio_route import (
    configurar_relatorio_routes
)

# Rota inicial do sistema.
from app.routes.routes import (
    configurar_rotas
)

# Rotas do dashboard.
from app.routes.dashboard_route import (
    configurar_dashboard_routes
)

# Rotas de movimentação de estoque.
from app.routes.movimentacao_route import (
    configurar_movimentacao_routes
)

# Rotas de configuração e gerenciamento da sinuca.
from app.routes.sinuca_route import (
    configurar_sinuca_routes
)

# Rotas de gerenciamento de usuários.
from app.routes.usuario_route import (
    configurar_usuario_routes
)


# ============================================================
# CRIAR A APLICAÇÃO FLASK
# ============================================================
# A instância 'app' representa a aplicação web.
# É nela que registramos rotas, configurações e comportamentos
# executados durante as requisições.
app = Flask(
    __name__,

    # Define a pasta em que o Flask encontrará os templates HTML.
    template_folder="app/templates",

    # Define a pasta dos arquivos estáticos, como CSS,
    # JavaScript e imagens.
    static_folder="app/static"
)


# ============================================================
# CONFIGURAÇÃO DA SESSÃO
# ============================================================
# A chave secreta é utilizada pelo Flask para assinar os dados
# de sessão armazenados pelo navegador.
#
# Mantive o valor original para não alterar a configuração
# durante esta refatoração.
#
# IMPORTANTE:
# Em produção, utilize uma chave forte obtida de uma variável
# de ambiente, em vez de manter uma chave fixa no código.
app.secret_key = "tcc_bar"


# ============================================================
# TRATAMENTO DE ERRO HTTP 403
# ============================================================
# O erro HTTP 403 significa que o acesso à página foi negado.
#
# Por exemplo, pode ocorrer quando um usuário autenticado
# tenta acessar uma rota cujo perfil não está autorizado.
@app.errorhandler(403)
def acesso_negado(error):
    """
    Exibe a página personalizada de acesso negado.
    """

    # Renderiza a página de erro e informa ao navegador
    # que a resposta possui o código HTTP 403.
    return render_template(
        "errors/403.html"
    ), 403


# ============================================================
# VERIFICAÇÃO GLOBAL DE LOGIN
# ============================================================
# O before_request é executado antes de cada requisição
# recebida pela aplicação Flask.
#
# A função abaixo permite o acesso às rotas livres definidas
# na lista e redireciona para o login quando não há um
# identificador de usuário na sessão.
#
# Essa verificação é global e complementa os decorators
# de autenticação utilizados nas rotas.
@app.before_request
def verificar_login():
    """
    Exige autenticação global, exceto nas rotas liberadas.
    """

    # Endpoints que podem ser acessados sem autenticação.
    #
    # 'login' corresponde ao endpoint da função de login.
    # 'static' corresponde ao endpoint utilizado para servir
    # arquivos estáticos, como CSS, JavaScript e imagens.
    rotas_livres = [
        "login",
        "static"
    ]

    # request.endpoint informa qual função de rota do Flask
    # está atendendo à requisição atual.
    #
    # Se o endpoint estiver na lista de rotas livres,
    # não será necessária outra verificação neste ponto.
    if request.endpoint in rotas_livres:
        return

    # Verifica se o identificador do usuário está armazenado
    # na sessão atual.
    if "usuario_id" not in session:

        # Sem um usuário identificado na sessão, o acesso
        # é interrompido e o navegador é enviado ao login.
        return redirect(
            "/login"
        )


# ============================================================
# REGISTRAR AS ROTAS DA APLICAÇÃO
# ============================================================
# Cada função abaixo registra no Flask as rotas do módulo
# correspondente.
#
# É importante executar essas chamadas durante a inicialização
# da aplicação, antes de iniciar o servidor.
#
# A ordem original foi preservada para reduzir o risco
# de mudanças no comportamento do sistema.


# Registra a rota inicial: "/".
configurar_rotas(app)

# Registra as rotas de clientes.
configurar_cliente_routes(app)

# Registra as rotas de produtos.
configurar_produto_routes(app)

# Registra as rotas de estoque.
configurar_estoque_routes(app)

# Registra as rotas de fornecedores.
configurar_fornecedor_routes(app)

# Registra as rotas de vendas.
configurar_venda_routes(app)

# Registra as rotas do carrinho.
configurar_carrinho_routes(app)

# Registra as rotas de contas pendentes.
configurar_conta_routes(app)

# Registra as rotas de vendas fiadas.
configurar_fiado_routes(app)

# Registra as rotas de relatórios.
configurar_relatorio_routes(app)

# Registra as rotas do dashboard.
configurar_dashboard_routes(app)

# Registra as rotas de movimentação de estoque.
configurar_movimentacao_routes(app)

# Registra as rotas de sinuca.
configurar_sinuca_routes(app)

# Registra as rotas de autenticação.
configurar_auth_routes(app)

# Registra as rotas de gerenciamento de usuários.
configurar_usuario_routes(app)


# ============================================================
# INICIAR O SERVIDOR
# ============================================================
# Esta condição verifica se o arquivo está sendo executado
# diretamente, em vez de ter sido importado por outro módulo.
#
# Quando executado diretamente, inicia o servidor Flask.
if __name__ == "__main__":

    # debug=True ativa o modo de depuração e permite que
    # o servidor reinicie automaticamente após alterações
    # no código.
    #
    # Utilize esse modo durante o desenvolvimento.
    # Não o utilize em produção.
    app.run(
        debug=True
    )
