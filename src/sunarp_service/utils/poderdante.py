from typing import Any, cast

from sunarp_service.models.types.dict import OtorganteJuridicoDict, OtorganteNaturalDict


def cast_poderdante_dict(
    info: dict[str, Any],
) -> OtorganteJuridicoDict | OtorganteNaturalDict:
    if "numero_ruc" in info:
        return cast(OtorganteJuridicoDict, info)
    if "documento" in info:
        return cast(OtorganteNaturalDict, info)
    raise ValueError("El diccionario no tiene la estructura esperada")
