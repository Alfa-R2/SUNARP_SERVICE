from ..models.types.tipo_documentos import TipoDocumento


def get_nombres_apellidos(nombre: str) -> tuple[str, str, str]:
    primer_nombre, segundo_nombre, primer_apellido, *segundo_apellido = nombre.split()
    pre_nombres = [primer_nombre, segundo_nombre]
    return " ".join(pre_nombres), primer_apellido, " ".join(segundo_apellido)
