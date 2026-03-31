from re import match

from pydantic import BaseModel, field_validator, model_validator
from typing_extensions import Self

from sunarp_service.helpers.convert import convert_tipo_documento
from sunarp_service.models.types.tipo_documentos import TipoDocumento


class ParticipanteNatural(BaseModel):
    pre_nombres: str
    primer_apellido: str
    segundo_apellido: str
    numero_documento: str
    tipo_documento: TipoDocumento

    def model_post_init(self, __context) -> None:
        """
        __context: Pydantic lo necesita por su interfaz interna.
        """
        if self.tipo_documento == "DNI DOCUMENTO NACIONAL DE IDENTIDAD":
            # ? Set the next attributes to '-' if the type of document is 'DOCUMENTO NACIONAL DE IDENTIDAD' because SID SUNARP will provide this information
            self.pre_nombres = "-"
            self.primer_apellido = "-"
            self.segundo_apellido = "-"

    @model_validator(mode="after")
    def validar_numero_documento(self) -> Self:
        """
        Validate the numero_documento.
        """
        if self.tipo_documento == "DNI DOCUMENTO NACIONAL DE IDENTIDAD":
            patron = r"^\d{8}$"
        elif self.tipo_documento == "CE CARNET DE EXTRANJERIA":
            patron = r"^\d{9}$"
        elif self.tipo_documento == "PS PASAPORTE":
            patron = r"^[A-Z]{1,2}\d{6,8}$"
        else:
            raise NotImplementedError("Tipo de documento no reconocido")

        if not match(patron, self.numero_documento):
            raise ValueError(
                f"'{self.numero_documento}' no es un número de documento válido para el tipo de documento '{self.tipo_documento}'"
            )
        return self
