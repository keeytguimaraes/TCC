# Importa funções do Flask
from flask import (
    render_template,
    request,
    redirect
)

# Importa controllers
from app.controllers.cliente_controller import (
    pegar_clientes,
    cadastrar_cliente_controller,
    excluir_cliente_controller,
    buscar_cliente_controller,
    editar_cliente_controller
)


# Função responsável por registrar as rotas
def configurar_cliente_routes(app):

    # ==========================
    # ROTA: LISTAR CLIENTES
    # ==========================
    @app.route("/cliente")
    def cliente():

        # Busca clientes do banco
        dados = pegar_clientes()

        # Envia dados para HTML
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

        # Atualiza tela
        return redirect("/cliente")


    # ==========================
    # ROTA: EXCLUIR CLIENTE
    # ==========================
    @app.route(
        "/cliente/excluir/<int:id_cliente>"
    )
    def excluir_cliente(id_cliente):

        # Exclui cliente
        excluir_cliente_controller(
            id_cliente
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

        # Volta para lista
        return redirect("/cliente")