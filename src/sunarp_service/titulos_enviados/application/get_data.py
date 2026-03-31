from pathlib import Path
from re import Pattern, compile

from loguru import logger
from patchright.sync_api import Download, ElementHandle, Locator, Page
from pypdf import PdfReader

from sunarp_service.titulos_enviados.entities.exceptions import (
    ErrorMessageFoundException,
)
from sunarp_service.titulos_enviados.entities.types import DOWNLOAD_PDF_SCRIPT
from sunarp_service.titulos_enviados.utils import get_cell_texts


class GetData:
    @classmethod
    def __extract_data_from_formulario_page(cls, temp_page: Page) -> tuple[
        str,
        str,
        str,
        str,
        str,
        str | None,
    ]:
        _NON_WHITESPACE_PATTERN: Pattern = compile(r"\S+")
        placa_partida: str | None = None
        acto: str = ""
        numero_titulo: str = ""
        fecha_documento: str = ""
        monto_pagado: str = ""
        area_registral: str = ""

        title_data_tbody: str = "form#j_id596338292_238b7354 > table:not([id]) > tbody"
        error_span_selector: str = 'span:has-text("MENSAJE DE ERROR")'
        loading_selectors: tuple[str, ...] = (title_data_tbody, error_span_selector)
        loading_element: Locator = temp_page.locator(", ".join(loading_selectors))
        loading_element.wait_for()

        if temp_page.is_visible(error_span_selector):
            raise ErrorMessageFoundException

        plates_label: Locator = temp_page.locator(
            "table#frmTitu\\:j_id596338292_238b6bdd"
        )
        plates_td: Locator = plates_label.locator("+ table > tbody > tr > td")
        if plates_td.is_visible():
            # NOTE: "BVH478 BVV358 ," like texts may be stripped like "BVH478 BVV358" or something like that.
            placa_partida = plates_td.inner_text()

        act_label: Locator = temp_page.locator("table#frmTitu\\:j_id596338292_238b6c7a")
        act_tr: Locator = act_label.locator("+ table > tbody > tr")
        act_td: Locator = act_tr.locator("> td", has_text=_NON_WHITESPACE_PATTERN)
        act_or_right, *extras = act_td.all_inner_texts()
        assert len(extras) < 2
        acto = act_or_right

        # NOTE: If not exactly 2 rows, this code block should be skipped, but i got no proof.
        title_data_row: Locator = temp_page.locator(f"{title_data_tbody} > tr")
        header, row = map(get_cell_texts, title_data_row.all())
        title_data: dict[str, str] = dict(zip(header, row))
        numero_titulo = title_data["Número de Título"]
        fecha_documento = title_data["Fecha y hora"]
        monto_pagado = title_data["Monto pagado"]

        legal_registration_table: str = "table#frmTitu\\:j_id596338292_238b64fe"
        checked_label: str = 'input[type="checkbox"]:checked + label'
        legal_registration_selector: str = f"{legal_registration_table} {checked_label}"
        legal_registration_label: Locator = temp_page.locator(
            legal_registration_selector
        )
        legal_registration: str = legal_registration_label.inner_text()
        area_registral = legal_registration.strip()

        return (
            acto,
            numero_titulo,
            fecha_documento,
            monto_pagado,
            area_registral,
            placa_partida,
        )

    @classmethod
    def extract_data_from_formulario_link(
        cls, page: Page, formulario_url: str, download_dir: Path | None = None
    ) -> tuple[
        str,
        str,
        str,
        str,
        str,
        str | None,
        Path | None,
    ]:
        temp_page: Page = page.context.new_page()
        formulario_path: Path | None = None

        try:
            temp_page.goto(formulario_url)
            temp_page.wait_for_load_state()
            data = cls.__extract_data_from_formulario_page(temp_page)

            if download_dir:
                formulario_path = download_dir / "FORMULARIO.pdf"
                temp_page.pdf(path=formulario_path)
                temp_page.close()

            return *data, formulario_path
        finally:
            if not temp_page.is_closed():
                temp_page.close()

    @logger.catch
    @staticmethod
    def get_codigo_tive(
        page: Page, td: ElementHandle, download_path: Path
    ) -> str | None:
        tive: str | None = None
        select: ElementHandle | None = td.query_selector("select")
        assert select

        option: ElementHandle | None = select.query_selector(
            'option:has-text("CARGO SOL")'
        )
        assert option

        value: str | None = option.get_attribute("value")
        assert value

        with page.context.expect_page() as tive_data_page_info:
            select.select_option(value)
        temp_page: Page = tive_data_page_info.value

        try:
            temp_page.wait_for_load_state()

            with temp_page.expect_download() as event_info:
                temp_page.evaluate(DOWNLOAD_PDF_SCRIPT)
            download: Download = event_info.value
            download.save_as(download_path)
            temp_page.close()

            pdf_text = PdfReader(download_path).pages[0].extract_text()
            if "TIVe" in pdf_text:
                pattern: Pattern = compile(r"(?<=\()\d{8}(?=\))")
                assert (_tive := pattern.search(pdf_text))
                tive = _tive.group()
                logger.info(f"{tive = }.")
        finally:
            if not temp_page.is_closed():
                temp_page.close()
            return tive

    @logger.catch
    @staticmethod
    def get_recibo_pago(
        page: Page, pagos_dropdown_option: ElementHandle, download_dir: Path
    ) -> Path:
        save_path: Path = download_dir / "RECIBO_INGRESO.pdf"
        pagos_dropdown_option.click()

        pago_anchor = pagos_dropdown_option.query_selector("a")
        assert pago_anchor

        with page.context.expect_page() as recibo_page_info:
            pago_anchor.click()

        recibo_page: Page = recibo_page_info.value
        page.wait_for_timeout(
            1000
        )  # NOTE: Wait for the pdf to load, otherwise the download may be empty.
        try:
            recibo_page.pdf(path=save_path)
            return save_path
        finally:
            if not recibo_page.is_closed():
                recibo_page.close()
