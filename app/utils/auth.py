from flask import (
    session,
    redirect,
    abort
)

from flask import request
from functools import wraps


def login_obrigatorio(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "usuario_id" not in session:

            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper


def perfil_obrigatorio(*perfis):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if session.get("perfil") not in perfis:

                abort(403)

            return func(*args, **kwargs)

        return wrapper

    return decorator