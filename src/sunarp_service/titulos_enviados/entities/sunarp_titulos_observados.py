from pathlib import Path

from patchright.sync_api import BrowserContext, Locator

from sunarp_service.titulos_enviados.application.get_sunarp_result import (
    GetSunarpResult,
)
from sunarp_service.titulos_enviados.entities.result import SIDSunarpSearchResult


class SunarpTitulosObservados:
    """
    A class to interact with the SUNARP Notarios Titulos Observados page.
    """

    def __init__(self, browser_ctx: BrowserContext, url_page: str) -> None:
        titulos_observados_page = browser_ctx.new_page()
        titulos_observados_page.goto(url_page, wait_until="networkidle")

        titulos_observados_page.wait_for_load_state(state="networkidle")

        self.page_titulos_observados = titulos_observados_page

    def __enter__(self) -> "SunarpTitulosObservados":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.page_titulos_observados.is_closed():
            self.page_titulos_observados.close()

    def find(
        self, numero_solicitud: str, downloads_dir: Path | None = None
    ) -> SIDSunarpSearchResult | None:
        page = self.page_titulos_observados

        request_number_input: Locator = page.locator("#nroSolicitud")
        request_number_input.fill(numero_solicitud)

        title_year_select: Locator = page.locator("#anioTitulo")
        title_year_option: Locator = title_year_select.locator("option")
        title_years = tuple(title_year_option.all_inner_texts())

        search_button: Locator = page.locator('button[onclick="buscar()"]')
        first_row_tbody_tr = page.locator("#row > tbody > tr").first
        for title_year in title_years:
            title_year_select.select_option(label=title_year)
            first_row_tbody_tr.wait_for(timeout=90_000)
            page.wait_for_timeout(500)

            with page.expect_response(
                "https://sid.sunarp.gob.pe/sid/bandeja.htm"
            ) as event_info:
                search_button.click()

            if not event_info.value.ok:
                raise Exception("Network error")

            page.wait_for_timeout(500)
            first_row_tbody_tr.wait_for()

            tr_class = first_row_tbody_tr.get_attribute("class")
            if tr_class == "empty":
                continue

            assert (tbody := page.wait_for_selector("#row > tbody"))
            assert (first_tr := tbody.query_selector("> tr:first-child"))

            return GetSunarpResult.from_titulo_observado_row(
                page, first_tr, downloads_dir
            )

        return None
