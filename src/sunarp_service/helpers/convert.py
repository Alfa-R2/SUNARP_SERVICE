from typing import cast

from ..models.types.actos_registrales import (
    ActoRegistral,
    __actos_registrales__,
    acto_registral_dict,
)
from ..models.types.estados_civiles import (
    EstadoCivil,
    __estados_civiles__,
    estado_civil_dict,
)
from ..models.types.nacionalidades import (
    Nacionalidad,
    __nacionalidades__,
    nacionalidad_dict,
)
from ..models.types.ocupaciones_profesiones import (
    ProfesionOcupacion,
    __ocupaciones_profesiones__,
    ocupaciones_profesiones_dict,
)
from ..models.types.oficinas_registrales import (
    OficinaRegistral,
    __oficinas_registrales__,
)
from ..models.types.services import Service, __servicios__
from ..models.types.tipo_documentos import (
    TipoDocumento,
    __tipos_documentos__,
    tipo_documento_dict,
)


def clean_string(string: str) -> str:
    return string.strip().upper()


def convert_servicio(servicio_raw: str) -> Service:
    servicio = servicio_raw.strip()

    if servicio not in __servicios__:
        raise ValueError(f"'{servicio}' no es un servicio válido")

    return cast(Service, servicio)


def convert_tipo_documento(tipo_documento_raw: str) -> TipoDocumento:
    tipo_documento = clean_string(tipo_documento_raw)

    if tipo_documento in __tipos_documentos__:
        return cast(TipoDocumento, tipo_documento)

    possible_tipo_documento = tipo_documento_dict.get(tipo_documento, None)

    if not possible_tipo_documento:
        raise ValueError(f"'{tipo_documento}' no es un tipo de documento válido")

    return possible_tipo_documento


def convert_acto_registral(acto_registral_raw: str) -> ActoRegistral:
    acto_registral = clean_string(acto_registral_raw)

    if acto_registral in __actos_registrales__:
        return cast(ActoRegistral, acto_registral)

    possible_acto_registral = acto_registral_dict.get(acto_registral, None)

    if not possible_acto_registral:
        raise ValueError(f"'{acto_registral}' no es un ActoRegistral válido")

    return possible_acto_registral


def convert_ocupacion(
    ocupacion_raw: str,
    strict: bool = True,
) -> ProfesionOcupacion:
    default: ProfesionOcupacion | None = (
        "OTRA ACTIVIDAD PARTICULAR" if not strict else None
    )
    ocupacion = clean_string(ocupacion_raw)

    if ocupacion in __ocupaciones_profesiones__:
        return cast(ProfesionOcupacion, ocupacion)

    possible_ocupacion_raw = ocupaciones_profesiones_dict.get(ocupacion, default)

    if not possible_ocupacion_raw:
        raise ValueError(f"'{ocupacion}' no es una ocupación válida")

    return possible_ocupacion_raw


def convert_nacionalidad(nacionalidad_raw: str) -> Nacionalidad:
    nacionalidad = clean_string(nacionalidad_raw)

    if nacionalidad in __nacionalidades__:
        return cast(Nacionalidad, nacionalidad)

    possible_nacionalidad_raw = nacionalidad_dict.get(nacionalidad, None)

    if not possible_nacionalidad_raw:
        raise ValueError(f"'{nacionalidad}' no es una nacionalidad válida")

    return possible_nacionalidad_raw


def convert_estado_civil(estado_civil_raw: str) -> EstadoCivil:
    estado_civil = clean_string(estado_civil_raw)

    if estado_civil in __estados_civiles__:
        return cast(EstadoCivil, estado_civil)

    possible_estado_civil_raw = estado_civil_dict.get(estado_civil, None)

    if not possible_estado_civil_raw:
        raise ValueError(f"'{estado_civil}' no es estado civil válido")
    return possible_estado_civil_raw


def convert_oficina_registral(
    oficina_registral_raw: str,
) -> OficinaRegistral:
    oficina_registral = clean_string(oficina_registral_raw)

    if oficina_registral not in __oficinas_registrales__:
        raise ValueError(f"'{oficina_registral}' no es una oficina registral válida")

    return cast(OficinaRegistral, oficina_registral)
