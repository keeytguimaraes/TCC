from flask import (
    render_template,
    request,
    redirect,
    session,
    flash
)

from app.controllers.auth_controller import (
    autenticar_usuario
)


def configurar_auth_routes(app):

    @app.route(
        "/login",
        methods=["GET", "POST"]
    )
    def login():

        if request.method == "POST":

            usuario = request.form.get(
                "usuario"
            )

            senha = request.form.get(
                "senha"
            )

            usuario_logado = (
                autenticar_usuario(
                    usuario,
                    senha
                )
            )

            print("USUARIO LOGADO:", usuario_logado)

            if usuario_logado:

                session["usuario_id"] = (
                    usuario_logado["id"]
                )

                session["nome"] = (
                    usuario_logado["nome"]
                )

                session["perfil"] = (
                    usuario_logado["perfil"]
                )

                print("PERFIL NA SESSAO:", session["perfil"])

                return redirect("/dashboard")

            flash(
                "Usuário ou senha inválidos",
                "error"
            )

        return render_template(
            "auth/login.html"
        )


    @app.route("/logout")
    def logout():

        session.clear()

        return redirect("/login")