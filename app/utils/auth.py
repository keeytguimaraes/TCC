
# ============================================================
# AUTENTICAÇÃO E CONTROLE DE ACESSO — SIGC
# ============================================================
# Este arquivo contém os decorators responsáveis por proteger
# as rotas da aplicação.
#
# Funcionalidades:
# - Verificar se o usuário está autenticado;
# - Restringir o acesso de acordo com o perfil do usuário.
#
# Autenticação responde à pergunta:
# "O usuário está conectado ao sistema?"
#
# Autorização responde à pergunta:
# "O usuário conectado tem permissão para acessar esta rota?"
# ============================================================


# Importa as ferramentas do Flask necessárias para controlar
# a sessão e o acesso às páginas.
from flask import (
    session,
    redirect,
    abort
)

# wraps preserva informações da função original quando ela
# é envolvida por um decorator.
from functools import wraps


# ============================================================
# DECORATOR: EXIGIR LOGIN
# ============================================================
def login_obrigatorio(func):
    """
    Exige que exista um usuário autenticado na sessão.

    Se a sessão não contiver 'usuario_id', o usuário será
    redirecionado para a página de login.

    Caso contrário, a função original da rota será executada.

    Parâmetros:
        func: função da rota que será protegida.
    """

    # Define a função intermediária que será executada
    # antes da função original da rota.
    @wraps(func)
    def wrapper(*args, **kwargs):

        # Verifica se o identificador do usuário está presente
        # na sessão atual.
        #
        # O sistema utiliza essa chave para reconhecer
        # que existe um usuário autenticado.
        if "usuario_id" not in session:

            # Se não houver usuário autenticado, interrompe
            # o fluxo da rota e redireciona para o login.
            return redirect("/login")

        # Se o identificador estiver presente, permite
        # a execução normal da função original.
        #
        # *args e **kwargs repassam os argumentos posicionais
        # e nomeados recebidos pela rota.
        return func(*args, **kwargs)

    # Retorna a função protegida para que o Flask a utilize
    # no lugar da função original da rota.
    return wrapper


# ============================================================
# DECORATOR: EXIGIR PERFIL AUTORIZADO
# ============================================================
def perfil_obrigatorio(*perfis):
    """
    Restringe uma rota aos perfis autorizados.

    Os perfis permitidos são informados ao aplicar o decorator.

    Exemplos:
        @perfil_obrigatorio("administrador")
        @perfil_obrigatorio("administrador", "gerente")

    Se o perfil armazenado na sessão não estiver entre
    os permitidos, a aplicação retorna o erro HTTP 403.

    Parâmetros:
        *perfis: conjunto de perfis autorizados para a rota.
    """

    # Cria o decorator que receberá a função da rota.
    def decorator(func):

        # Define a função intermediária responsável
        # por verificar o perfil antes de executar a rota.
        @wraps(func)
        def wrapper(*args, **kwargs):

            # Recupera o perfil armazenado na sessão.
            #
            # session.get("perfil") retorna None se a chave
            # não existir, evitando um erro de chave ausente.
            perfil_usuario = session.get("perfil")

            # Verifica se o perfil atual está entre os perfis
            # permitidos na aplicação do decorator.
            if perfil_usuario not in perfis:

                # Retorna o erro HTTP 403 (Forbidden),
                # indicando que o acesso não está autorizado.
                abort(403)

            # Se o perfil estiver autorizado, executa
            # a função original da rota.
            return func(*args, **kwargs)

        # Retorna a função protegida pelo controle de perfil.
        return wrapper

    # Retorna o decorator configurado com os perfis recebidos.
    return decorator
