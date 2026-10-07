from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)
# Importa funções do Flask
from flask import (
    render_template,
    request,
    redirect,
    flash
)

# Importa controllers
from app.controllers.cliente_controller import (
    pegar_clientes,
    cadastrar_cliente_controller,
    desativar_cliente_controller,
    buscar_cliente_controller,
    editar_cliente_controller,
    listar_clientes_inativos_controller,
    reativar_cliente_controller
)

# Função responsável por registrar as rotas
def configurar_cliente_routes(app):

    # ==========================
    # ROTA: LISTAR CLIENTES
    # ==========================
    @app.route("/cliente")
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador",
    "gerente"
)
    def cliente():

        dados = pegar_clientes()

        return render_template(
        "cliente/cliente.html",
        clientes=dados
    )


    # ==========================
    # ROTA: CADASTRAR CLIENTE
    # ==========================
    @app.route(
        "/cliente/cadastrar",
        methods=["POST"]
    )
    def cadastrar_cliente():

        # Pega nome do formulário
        nome = request.form.get("nome")

        # Salva no banco
        cadastrar_cliente_controller(nome)

        flash(
    "Cliente cadastrado com sucesso!",
    "success"
)

        # Atualiza tela
        return redirect("/cliente")

    # ==========================
    # ROTA: ABRIR TELA EDITAR
    # ==========================
    @app.route(
        "/cliente/editar/<int:id_cliente>"
    )
    def tela_editar_cliente(id_cliente):

        # Busca cliente
        cliente = buscar_cliente_controller(
            id_cliente
        )

        # Abre HTML
        return render_template(
            "cliente/editar_cliente.html",
            cliente=cliente
        )


    # ==========================
    # ROTA: SALVAR EDIÇÃO
    # ==========================
    @app.route(
        "/cliente/editar/<int:id_cliente>",
        methods=["POST"]
    )
    def editar_cliente(id_cliente):

        # Pega nome digitado
        nome = request.form.get(
            "nome"
        )

        # Atualiza no banco
        editar_cliente_controller(
            id_cliente,
            nome
        )

        flash(
    "Cliente atualizado com sucesso!",
    "success"
)

        # Volta para lista
        return redirect("/cliente")
    
# =========================
# ROTA DE DESATIVAR CLIENTE
# =========================
    @app.route(
    "/cliente/desativar/<int:cliente_id>",
    methods=["POST"]
)
    def desativar_cliente(cliente_id):

        desativar_cliente_controller(
        cliente_id
    )

        return redirect("/cliente")
    
# =========================
# ROTA DE LISTAR CLIENTES INATIVOS
# =========================
    @app.route("/cliente/inativos")
    def clientes_inativos():

        dados = listar_clientes_inativos_controller()

        return render_template(
        "cliente/clientes_inativos.html",
        clientes=dados
    )
# =========================
# REATIVAR CLIENTE
# =========================
    @app.route(
    "/cliente/reativar/<int:cliente_id>",
    methods=["POST"]
)
    def reativar_cliente(cliente_id):

        reativar_cliente_controller(
        cliente_id
    )

        return redirect(
        "/cliente/inativos"
    )