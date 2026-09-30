from werkzeug.security import (
    check_password_hash
)

from app.models.auth_model import (
    buscar_usuario_por_login
)


def autenticar_usuario(
    usuario,
    senha
):

    usuario_db = buscar_usuario_por_login(
        usuario
    )

    if not usuario_db:

        return None

    if not check_password_hash(
        usuario_db["senha"],
        senha
    ):

        return None

    return usuario_db