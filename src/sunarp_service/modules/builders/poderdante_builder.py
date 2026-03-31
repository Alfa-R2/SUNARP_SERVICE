from sunarp_service.helpers.convert import (
    convert_estado_civil,
    convert_nacionalidad,
    convert_ocupacion,
    convert_oficina_registral,
    convert_tipo_documento,
)
from sunarp_service.helpers.info import get_nombres_apellidos
from sunarp_service.models.participants.participantes import (
    Otorgante,
    ParticipanteJuridico,
)
from sunarp_service.models.types.dict import OtorganteJuridicoDict, OtorganteNaturalDict


class PoderdanteBuilder:
    @staticmethod
    def make_poderdante_juridico_from_dict(
        data: OtorganteJuridicoDict,
    ) -> ParticipanteJuridico:
        """
        The bussiness logic of the page specifies that the type of participant is "APODERADO" when a poderdante is a legal entity.
        """
        oficina_registral = data["oficina_registral"]

        if isinstance(oficina_registral, str):
            oficina_registral = convert_oficina_registral(oficina_registral)

        return ParticipanteJuridico(
            numero_ruc=data["numero_ruc"],
            partida_registral=data["partida_registral"],
            oficina_registral=oficina_registral,
            tipo_participante="APODERADO",
        )

    @staticmethod
    def make_a_poderdante_natural_from_dict(
        data: OtorganteNaturalDict, strict: bool = True
    ) -> Otorgante:
        """
        Args:
            data (dict): Dictionary containing the data of the poderdante.
            strict (bool): If True, the function will raise an error if the ocupacion is not valid, otherwise it will return "OTRA ACTIVIDAD PARTICULAR".
        """

        pre_nombres, primer_apellido, segundo_apellido = get_nombres_apellidos(
            data["nombre"]
        )
        ocupacion = data["ocupacion"]
        nacionalidad = data["nacionalidad"]
        numero_documento = data["documento"]
        estado_civil = data["estado_civil"]
        tipo_documento = data["tipo_documento"]

        if isinstance(nacionalidad, str):
            nacionalidad = convert_nacionalidad(nacionalidad)
        if isinstance(ocupacion, str):
            ocupacion = convert_ocupacion(ocupacion, strict)
        if isinstance(estado_civil, str):
            estado_civil = convert_estado_civil(estado_civil)
        if isinstance(tipo_documento, str):
            tipo_documento = convert_tipo_documento(tipo_documento)

        return Otorgante(
            pre_nombres=pre_nombres,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            nacionalidad=nacionalidad,
            estado_civil=estado_civil,
            ocupacion=ocupacion,
            numero_documento=numero_documento,
            tipo_documento=tipo_documento,
            tipo_participante="PODERDANTE",
        )
