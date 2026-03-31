from pathlib import Path

from patchright.sync_api import ElementHandle, Locator, Page

from sunarp_service.titulos_enviados.application.get_sunarp_result import (
    GetSunarpResult,
)
from sunarp_service.titulos_enviados.entities.result import SIDSunarpSearchResult


class SunarpTitulosEnviados:
    """
    A class to interact with the SUNARP Notarios Titulos Enviados a la Sunarp page.
    """

    def __init__(self, page: Page):
        self.page_titulos_enviados = page

    def __enter__(self) -> "SunarpTitulosEnviados":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.page_titulos_enviados.is_closed():
            self.page_titulos_enviados.close()

    def find(
        self, numero_solicitud: str, download_dir: Path | None = None
    ) -> SIDSunarpSearchResult | None:
        """
        Find the first title in the list of sent titles and click on it.
        """
        page = self.page_titulos_enviados

        page.locator("#nroSolicitud").fill(numero_solicitud)
        page.locator("#anioTitulo").select_option(label="Seleccionar")

        title_status_select: Locator = page.locator("#esttitulo")
        option: Locator = title_status_select.locator(
            "option", has_not_text="SOLICITUDES PENDIENTES"
        )
        labels: tuple[str, ...] = tuple(map(str.strip, option.all_inner_texts()))

        search_button: Locator = page.locator('button[onclick="buscar()"]')

        for pending_title_status in labels:
            title_status_select.select_option(label=pending_title_status)

            with page.expect_response(
                "https://sid.sunarp.gob.pe/sid/bandeja.htm"
            ) as event_info:
                search_button.click()

            if not event_info.value.ok:
                raise Exception("Network error")

            page.wait_for_timeout(1000)

            odd_row = page.locator("tr.odd")
            if odd_row.count() != 1:
                continue

            tbody_locator: Locator = page.locator("#row > tbody")
            tbody_locator.wait_for()
            tbody_handle: ElementHandle = tbody_locator.element_handle()
            first_row, *other_rows = tbody_handle.query_selector_all("> tr.odd")
            assert not other_rows

            return GetSunarpResult.from_titulo_enviado_row(
                page, pending_title_status, first_row, download_dir
            )

        return None
