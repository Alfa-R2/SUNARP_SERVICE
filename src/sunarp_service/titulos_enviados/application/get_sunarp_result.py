from pathlib import Path

from patchright.sync_api import ElementHandle, Page

from sunarp_service.titulos_enviados.entities.result import SIDSunarpSearchResult

from .get_data import GetData


class GetSunarpResult:

    @staticmethod
    def from_titulo_enviado_row(
        page: Page,
        pending_title_status: str,
        row: ElementHandle,
        download_dir: Path | None = None,
    ) -> SIDSunarpSearchResult:
        cells: list[ElementHandle] = row.query_selector_all("td")
        texts: tuple[str, ...] = tuple(c.inner_text().strip() for c in cells)
        numero_solicitud: str = texts[1]
        oficina_registral: str = texts[3]
        acto_registral: str = texts[4]
        solicitud_inscripcion: ElementHandle = cells[12]
        tive: str | None = None
        tive_file_path: Path | None = None

        assert (anchor := solicitud_inscripcion.query_selector("a"))
        assert (formulario_link := anchor.get_attribute("href"))

        recibo_pago_path: Path | None = (
            GetData.get_recibo_pago(page, cells[13], download_dir)
            if download_dir
            else None
        )

        if download_dir:
            tive_file_path = download_dir / "TIVE_CODE.pdf"
            tive = GetData.get_codigo_tive(page, cells[11], tive_file_path)

        extra_data = GetData.extract_data_from_formulario_link(
            page, formulario_link, download_dir
        )

        return SIDSunarpSearchResult(
            pending_title_status,
            numero_solicitud,
            oficina_registral,
            acto_registral,
            tive,
            *extra_data,
            recibo_pago_file=recibo_pago_path,
            tive_file_path=tive_file_path,
        )

    @staticmethod
    def from_titulo_observado_row(
        page: Page,
        row: ElementHandle,
        download_dir: Path | None = None,
    ) -> SIDSunarpSearchResult:
        # NOTE: Element handle is used to read rows to prevent sorting bug with locators.
        cells = row.query_selector_all("td")
        cells_txt = tuple(cell.inner_text().strip() for cell in cells)

        numero_solicitud = cells_txt[1]
        oficina_registral = cells_txt[3]
        acto_registral = cells_txt[4].strip()
        plazo_subsanar = cells_txt[8]
        eleven = cells[11]

        assert (anchor := eleven.query_selector("a"))
        assert (href := anchor.get_attribute("href"))

        extra_data = GetData.extract_data_from_formulario_link(page, href, download_dir)
        return SIDSunarpSearchResult(
            "OBSERVADO",
            numero_solicitud,
            oficina_registral,
            acto_registral,
            None,
            *extra_data,
            plazo_subsanar=plazo_subsanar,
        )
