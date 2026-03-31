from dataclasses import dataclass
from pathlib import Path


@dataclass
class SIDSunarpSearchResult:
    estado_registral: str
    numero_solicitud: str
    oficina_registral: str
    acto_registral: str
    tive: str | None
    acto: str
    nro_titulo: str
    fecha_documento: str
    monto_pagado: str
    area_registral: str
    placa_partida: str | None
    formulario_pdf: Path | None
    plazo_subsanar: str | None = None
    recibo_pago_file: Path | None = None
    tive_file_path: Path | None = None

    def __post_init__(self):
        self.nro_titulo = self.nro_titulo.replace(
            " ", ""
        ).strip()  # expected format: "2023-00000000"

    @property
    def anio_titulo(self) -> str:
        return self.nro_titulo.split("-")[0]

    @property
    def numero_titulo(self) -> str:
        return self.nro_titulo.split("-")[1]

    @property
    def downloaded_files(self) -> tuple[Path, ...]:
        files: list[Path] = [
            file_path
            for file_path in (
                self.formulario_pdf,
                self.recibo_pago_file,
                self.tive_file_path,
            )
            if file_path is not None
        ]

        return tuple(files)
