from re import match

from pydantic import BaseModel, field_validator
from stdnum.pe.ruc import validate  # type: ignore[import]

from sunarp_service.models.types.tipo_participantes import (
    TipoParticipanteFavorecido,
    TipoParticipanteOtorgante,
)

from ..types.estados_civiles import EstadoCivil
from ..types.nacionalidades import Nacionalidad
from ..types.ocupaciones_profesiones import ProfesionOcupacion
from ..types.oficinas_registrales import OficinaRegistral
from .core.participante_natural import ParticipanteNatural


class ParticipanteJuridico(BaseModel):
    numero_ruc: str
    partida_registral: str
    oficina_registral: OficinaRegistral
    tipo_participante: TipoParticipanteFavorecido

    @field_validator("partida_registral", mode="before")
    @classmethod
    def validate_partida_registral(cls, value_raw: str) -> str:
        value = value_raw.strip()
        posible_matched = match(r"\d{8}", value)
        if not posible_matched:
            raise ValueError(f"'{value_raw}' no es una partida registral válida")
        return posible_matched.group()

    @field_validator("numero_ruc", mode="before")
    @classmethod
    def validate_numero_ruc(cls, value_raw: str) -> str:
        value = value_raw.strip()
        try:
            validate(value)
        except Exception as e:
            raise ValueError(f"'{value_raw}' no es un RUC válido") from e
        return value


class Favorecido(ParticipanteNatural):
    tipo_participante: TipoParticipanteFavorecido


class Otorgante(ParticipanteNatural):
    tipo_participante: TipoParticipanteOtorgante
    nacionalidad: Nacionalidad
    estado_civil: EstadoCivil
    ocupacion: ProfesionOcupacion
