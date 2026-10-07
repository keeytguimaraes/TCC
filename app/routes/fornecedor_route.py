from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)
# Importa Flask
from flask import (

    render_template,
    request,
    redirect,
    flash
)

# Importa controller
from app.controllers.fornecedor_controller import (

    pegar_fornecedores,
    cadastrar_fornecedor_controller,

    pegar_fornecedor_por_id,
    editar_fornecedor_controller,

    pegar_fornecedores_inativos,
    reativar_fornecedor,
    desativar_fornecedor_controller
)


# ==========================
# CONFIGURAR ROTAS
# ==========================
def configurar_fornecedor_routes(app):

    # ==========================
    # LISTAR FORNECEDORES
    # ==========================
    @app.route("/fornecedor")
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador",
    "gerente"
)
    def fornecedor():

        # Busca fornecedores
        dados = pegar_fornecedores()

        # Envia HTML
        return render_template(

            "fornecedor/fornecedor.html",

            fornecedores=dados
        )

    # ==========================
    # CADASTRAR FORNECEDOR
    # ==========================
    @app.route(
        "/fornecedor/cadastrar",
        methods=["POST"]
    )
    def cadastrar_fornecedor_route():

        # Nome
        nome = request.form.get(
            "nome"
        )

        # Telefone
        telefone = request.form.get(
            "telefone"
        )

        # Observação
        observacao = request.form.get(
            "observacao"
        )

        # Envia controller
        cadastrar_fornecedor_controller(

            nome,
            telefone,
            observacao
        )

        flash(
    "Fornecedor cadastrado com sucesso!",
    "success"
)

        # Atualiza página
        return redirect(
            "/fornecedor"
        )

    # ==========================
    # EDITAR FORNECEDOR
    # ==========================
    @app.route(
        "/fornecedor/editar/<int:id_fornecedor>",
        methods=["GET", "POST"]
    )
    def editar_fornecedor_route(

        id_fornecedor
    ):

        # ----------------------
        # SE FOR POST
        # SALVA ALTERAÇÃO
        # ----------------------
        if request.method == "POST":

            # Nome
            nome = request.form.get(
                "nome"
            )

            # Telefone
            telefone = request.form.get(
                "telefone"
            )

            # Observação
            observacao = request.form.get(
                "observacao"
            )

            # Atualiza fornecedor
            editar_fornecedor_controller(

                id_fornecedor,

                nome,
                telefone,
                observacao
            )

            flash(
    "Fornecedor atualizado com sucesso!",
    "success"
)

            # Volta página
            return redirect(
                "/fornecedor"
            )

        # ----------------------
        # SE FOR GET
        # ABRE TELA
        # ----------------------
        fornecedor = (
            pegar_fornecedor_por_id(
                id_fornecedor
            )
        )

        # Abre HTML
        return render_template(

            "fornecedor/editar_fornecedor.html",

            fornecedor=fornecedor
        )
    
    @app.route(
    "/fornecedor/inativos"
)
    def fornecedores_inativos():

        fornecedores = (
        pegar_fornecedores_inativos()
    )

        return render_template(
        "fornecedor/inativar_fornecedor.html",
        fornecedores=fornecedores
    )

    @app.route(
    "/fornecedor/reativar/<int:id>"
)
    def reativar(id):

        try:

            reativar_fornecedor(
            id
        )

            flash(
            "Fornecedor reativado com sucesso!",
            "success"
        )

        except Exception:

            flash(
            "Erro ao reativar fornecedor.",
            "danger"
        )

        return redirect(
        "/fornecedor/inativos"
    )

    @app.route(
    "/fornecedor/desativar/<int:id>"
)
    def desativar(id):

        try:

            desativar_fornecedor_controller(
            id
        )

            flash(
            "Fornecedor desativado com sucesso!",
            "success"
        )

        except Exception:

            flash(
            "Erro ao desativar fornecedor.",
            "danger"
        )

        return redirect(
        "/fornecedor"
    )