
# ============================================================
# FORMATADORES — SIGC
# ============================================================
# Este arquivo reúne funções auxiliares para formatar valores
# antes de apresentá-los nas páginas e nos relatórios do sistema.
#
# A função atual formata valores numéricos como moeda brasileira
# (Real - R$), utilizando ponto para separar milhares e vírgula
# para separar as casas decimais.
# ============================================================


# ============================================================
# FORMATAR VALOR COMO MOEDA BRASILEIRA
# ============================================================
def moeda(valor):
    """
    Converte um valor numérico para o formato monetário brasileiro.

    Parâmetros:
        valor: valor que pode ser convertido para float.

    Retorno:
        Uma string formatada no padrão R$ 1.234,56.

    Exemplo:
        moeda(1234.56) retorna "R$ 1.234,56".
    """

    # Converte o valor recebido para float e formata com:
    # - duas casas decimais;
    # - vírgula como separador de milhares inicialmente;
    # - ponto como separador decimal inicialmente.
    #
    # Exemplo intermediário:
    # 1234.56 -> "1,234.56"
    valor_formatado = f"{float(valor):,.2f}"

    # Substitui temporariamente a vírgula por "X".
    # Isso evita que a substituição seguinte confunda
    # os separadores de milhares e de casas decimais.
    valor_formatado = valor_formatado.replace(
        ",",
        "X"
    )

    # Substitui o ponto decimal por vírgula, conforme
    # a convenção monetária brasileira.
    valor_formatado = valor_formatado.replace(
        ".",
        ","
    )

    # Substitui o marcador temporário "X" por ponto,
    # que será utilizado como separador de milhares.
    valor_formatado = valor_formatado.replace(
        "X",
        "."
    )

    # Adiciona o símbolo da moeda brasileira ao resultado.
    return f"R$ {valor_formatado}"
