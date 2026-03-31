from typing import TypedDict

OtorganteNaturalDict = TypedDict(
    "OtorganteNaturalDict",
    {
        "nombre": str,
        "documento": str,
        "tipo_documento": str,
        "estado_civil": str,
        "nacionalidad": str,
        "ocupacion": str,
    },
)
OtorganteJuridicoDict = TypedDict(
    "OtorganteJuridicoDict",
    {
        "oficina_registral": str,
        "numero_ruc": str,
        "partida_registral": str,
    },
)

FavorecidoNaturalDict = TypedDict(
    "FavorecidoNaturalDict",
    {
        "nombre": str,
        "documento": str,
        "tipo_documento": str,
    },
)
