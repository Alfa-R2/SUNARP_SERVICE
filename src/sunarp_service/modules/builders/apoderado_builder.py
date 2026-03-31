from sunarp_service.helpers.convert import convert_tipo_documento
from sunarp_service.helpers.info import get_nombres_apellidos
from sunarp_service.models.participants.participantes import Favorecido
from sunarp_service.models.types.dict import FavorecidoNaturalDict


class ApoderadoBuilder:
    @staticmethod
    def make_apoderado_from_dict(data: FavorecidoNaturalDict) -> Favorecido:
        pre_nombres, primer_apellido, segundo_apellido = get_nombres_apellidos(
            data["nombre"]
        )

        numero_documento = data["documento"]
        tipo_documento = data["tipo_documento"]

        if isinstance(tipo_documento, str):
            tipo_documento = convert_tipo_documento(tipo_documento)

        return Favorecido(
            pre_nombres=pre_nombres,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            numero_documento=numero_documento,
            tipo_documento=tipo_documento,
            tipo_participante="APODERADO",
        )
