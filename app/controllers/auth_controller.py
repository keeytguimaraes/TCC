# Importa a função responsável por verificar
# se a senha digitada corresponde ao hash
# armazenado no banco de dados.
from werkzeug.security import (
    check_password_hash
)

# Importa a função do model responsável
# por buscar um usuário através do login.
from app.models.auth_model import (
    buscar_usuario_por_login
)


# ==================================================
# AUTENTICAR USUÁRIO
# ==================================================
#
# Esta função é responsável por validar
# as credenciais informadas na tela de login.
#
# Fluxo:
#
# 1. Recebe usuário e senha digitados.
# 2. Busca o usuário no banco de dados.
# 3. Verifica se o usuário existe.
# 4. Verifica se a senha está correta.
# 5. Retorna os dados do usuário autenticado.
#
# Caso o usuário não exista ou a senha
# esteja incorreta, retorna None.
#
# ==================================================

def autenticar_usuario(
    usuario,
    senha
):

    # Busca no banco de dados um usuário
    # que possua o login informado.
    usuario_db = buscar_usuario_por_login(
        usuario
    )

    # Verifica se o usuário foi encontrado.
    #
    # Caso nenhum registro seja retornado,
    # interrompe o processo de autenticação.
    if not usuario_db:

        return None

    # Compara a senha digitada pelo usuário
    # com a senha criptografada armazenada
    # no banco de dados.
    #
    # Se forem diferentes, o login é negado.
    if not check_password_hash(
        usuario_db["senha"],
        senha
    ):

        return None

    # Retorna os dados completos do usuário.
    #
    # Essas informações serão utilizadas
    # para criar a sessão do usuário
    # após o login ser realizado.
    return usuario_db