from typing import Literal

type EstadoCivil = Literal["SOLTERO(A)", "CASADO(A)", "VIUDO(A)", "DIVORCIADO(A)"]

__estados_civiles__ = ("SOLTERO(A)", "CASADO(A)", "VIUDO(A)", "DIVORCIADO(A)")

estado_civil_dict: dict[str, EstadoCivil] = {
    "SOLTERO": "SOLTERO(A)",
    "CASADO": "CASADO(A)",
    "VIUDO": "VIUDO(A)",
    "DIVORCIADO": "DIVORCIADO(A)",
    "SOLTERA": "SOLTERO(A)",
    "CASADA": "CASADO(A)",
    "VIUDA": "VIUDO(A)",
    "DIVORCIADA": "DIVORCIADO(A)",
}
