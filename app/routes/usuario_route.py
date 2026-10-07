from flask import (
    render_template,
    request,
    redirect,
    flash,
    session
)

from app.controllers.usuario_controller import (
    pegar_usuarios,
    cadastrar_usuario_controller,
    usuario_existe,
    buscar_usuario_controller,
    editar_usuario_controller,
    desativar_usuario_controller,
    listar_usuarios_inativos_controller,
    reativar_usuario_controller,
    alterar_senha_usuario_controller
)

from app.utils.auth import (
    login_obrigatorio,
    perfil_obrigatorio
)


def configurar_usuario_routes(app):

    @app.route("/usuario")
    @login_obrigatorio
    @perfil_obrigatorio(
        "administrador"
    )
    def usuario():

        dados = pegar_usuarios()

        return render_template(
            "usuario/usuario.html",
            usuarios=dados
        )
    
    @app.route(
    "/usuario/cadastrar"
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def tela_cadastrar_usuario():

        return render_template(
        "usuario/cadastrar_usuario.html"
    )

    @app.route(
    "/usuario/cadastrar",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def cadastrar_usuario():

        nome = request.form.get(
        "nome"
    )

        usuario = request.form.get(
        "usuario"
    )
        
        if usuario_existe(usuario):

         flash(
        "Já existe um usuário com esse login.",
        "error"
    )

         return redirect(
        "/usuario/cadastrar"
    )

        senha = request.form.get(
        "senha"
    )

        confirmar_senha = request.form.get(
        "confirmar_senha"
    )

        perfil = request.form.get(
        "perfil"
    )

    # VALIDAR SENHAS

        if senha != confirmar_senha:

            flash(
            "As senhas não coincidem.",
            "error"
        )

            return redirect(
            "/usuario/cadastrar"
        )

        cadastrar_usuario_controller(
        nome,
        usuario,
        senha,
        perfil
    )

        flash(
        "Usuário cadastrado com sucesso!",
        "success"
    )

        return redirect(
        "/usuario"
    )

    @app.route(
    "/usuario/editar/<int:id_usuario>"
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def tela_editar_usuario(
    id_usuario
):

        usuario = buscar_usuario_controller(
        id_usuario
    )
    
        return render_template(
        "usuario/editar_usuario.html",
        usuario=usuario
    )

    @app.route(
    "/usuario/editar/<int:id_usuario>",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def editar_usuario(
    id_usuario
):

        nome = request.form.get(
        "nome"
    )

        usuario = request.form.get(
        "usuario"
    )

        perfil = request.form.get(
        "perfil"
    )
    
        editar_usuario_controller(
        id_usuario,
        nome,
        usuario,
        perfil
    )

        flash(
        "Usuário atualizado com sucesso!",
        "success"
    )

        return redirect(
        "/usuario"
    )

    @app.route(
    "/usuario/desativar/<int:id_usuario>",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def desativar_usuario(
    id_usuario
):

    # Proteção:
    # administrador não pode
    # desativar a si mesmo

        if (
        id_usuario
        ==
    session["usuario_id"]
    ):

            flash(
            "Você não pode desativar seu próprio usuário.",
            "error"
        )

            return redirect(
            "/usuario"
        )

        desativar_usuario_controller(
        id_usuario
    )

        flash(
        "Usuário desativado com sucesso!",
        "success"
    )

        return redirect(
        "/usuario"
    )

    @app.route("/usuario/inativos")
    @login_obrigatorio
    @perfil_obrigatorio("administrador")
    def usuarios_inativos():

        dados = (
        listar_usuarios_inativos_controller()
    )

        return render_template(
        "usuario/usuarios_inativos.html",
        usuarios=dados
    )

    @app.route(
    "/usuario/reativar/<int:id_usuario>",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio("administrador")
    def reativar_usuario(
    id_usuario
):

        reativar_usuario_controller(
        id_usuario
    )

        flash(
        "Usuário reativado com sucesso!",
        "success"
    )

        return redirect(
        "/usuario/inativos"
    )

    @app.route(
    "/usuario/senha/<int:id_usuario>"
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def tela_alterar_senha(
    id_usuario
):

        usuario = buscar_usuario_controller(
        id_usuario
    )

        return render_template(
        "usuario/alterar_senha.html",
        usuario=usuario
    )

    
    @app.route(
    "/usuario/senha/<int:id_usuario>",
    methods=["POST"]
)
    @login_obrigatorio
    @perfil_obrigatorio(
    "administrador"
)
    def alterar_senha(
    id_usuario
):

        senha = request.form.get(
        "senha"
    )

        confirmar_senha = request.form.get(
        "confirmar_senha"
    )

        if senha != confirmar_senha:

            flash(
            "As senhas não coincidem.",
            "error"
        )

            return redirect(
            f"/usuario/senha/{id_usuario}"
        )

        alterar_senha_usuario_controller(
        id_usuario,
        senha
    )
    
        flash(
        "Senha alterada com sucesso!",
        "success"
    )

        return redirect(
        "/usuario"
    )