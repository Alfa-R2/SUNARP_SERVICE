from pathlib import Path

from pydantic import BaseModel, field_validator

from sunarp_service.helpers.convert import (
    convert_acto_registral,
    convert_oficina_registral,
    convert_servicio,
)
from sunarp_service.models.participants.participantes import (
    Favorecido,
    Otorgante,
    ParticipanteJuridico,
)

from .actos_registrales import ActoRegistral
from .oficinas_registrales import OficinaRegistral
from .services import Service


class Solicitud(BaseModel):
    """
    A class to represent a SUNARP Notarios Solicitud.

    Attributes:
        servicio (Service): Services that Sunarp offers.
        acto_registral (ActoRegistral): Acto registral of the service.
        oficina_registral (OficinaRegistral): Oficina registral of the service.
        parte_notarial (str): Path of the Parte notarial.
        formulando_reserva (str): Extra information.
        liquidacion (str): Liquidacion of the service.
        correo_ciudadano (str): Email of the citizen to notify.
        participantes (list[ParticipanteJuridico | Otorgante | Favorecido]): Participants of the service.
    """

    servicio: Service
    acto_registral: ActoRegistral
    oficina_registral: OficinaRegistral
    parte_notarial: Path
    formulando_reserva: str
    liquidacion: str
    correo_ciudadano: str
    participantes: list[ParticipanteJuridico | Otorgante | Favorecido]

    @field_validator("servicio", mode="before")
    @classmethod
    def cast_servicio(cls, value_raw) -> Service:
        return convert_servicio(value_raw)

    @field_validator("acto_registral", mode="before")
    @classmethod
    def cast_acto_registral(cls, value_raw) -> ActoRegistral:
        return convert_acto_registral(value_raw)

    @field_validator("oficina_registral", mode="before")
    @classmethod
    def cast_oficina_registral(cls, value_raw) -> OficinaRegistral:
        return convert_oficina_registral(value_raw)
