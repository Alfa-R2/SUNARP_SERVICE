from patchright.sync_api import BrowserContext

from sunarp_service.titulos_enviados.entities.sunarp_titulos_observados import (
    SunarpTitulosObservados,
)

from .models.sunarp_ingreso_solicitud import SunarpIngresoSolicitud
from .titulos_enviados.sunarp_titulos_enviados import SunarpTitulosEnviados


class SunarpNotario:
    """
    A class to interact with the SID SUNARP Notarios service.

    Attributes:
        browser_ctx (BrowserContext): Playwright browser context.
        page (Page): Playwright page.
    """

    BASE_URL_SID = "https://sid.sunarp.gob.pe/sid"
    BASE_SECTION_URL = f"{BASE_URL_SID}/bandeja.htm?method="

    LOGIN_URL = f"{BASE_URL_SID}/sesion.htm"
    INGRESO_SOLICITUD_INSCRIPCION__URL = f"{BASE_SECTION_URL}registroActo"
    TITULOS_ENVIADOS_URL = f"{BASE_SECTION_URL}buscarBandeja&tiBandeja=S"
    TITULOS_OBSERVADOS_URL = f"{BASE_SECTION_URL}buscarObservados"

    def __init__(self, browser_ctx: BrowserContext) -> None:
        self.browser_ctx = browser_ctx
        self.page = self.browser_ctx.new_page()

    def login(self, username: str, password: str) -> None:
        """
        Login to the SUNARP Notarios service.

        Args:
            username (str): Username to login.
            password (str): Password to login.
        """
        page_login = self.page
        page_login.goto(self.LOGIN_URL)

        username_input = page_login.locator("#user")
        password_input = page_login.locator("#pass")
        button_submit = page_login.locator('input[type="button"]')

        username_input.wait_for()
        password_input.wait_for()
        button_submit.wait_for()

        username_input.fill(username)
        password_input.fill(password)
        button_submit.click()

        page_login.wait_for_selector('div:has-text("INSTITUCIÓN:")')

    def go_to_ingreso_solicitud_inscripcion_page(self) -> SunarpIngresoSolicitud:
        """
        Redirect to the SUNARP Notarios Ingreso Solicitud Inscripcion page and returns it.
        """
        ingreso_solicitud_page = self.browser_ctx.new_page()
        ingreso_solicitud_page.goto(
            self.INGRESO_SOLICITUD_INSCRIPCION__URL, wait_until="networkidle"
        )

        ingreso_solicitud_page.wait_for_load_state(state="networkidle")
        return SunarpIngresoSolicitud(ingreso_solicitud_page)

    def go_to_titulos_enviados(self) -> SunarpTitulosEnviados:
        """
        Redirect to the SUNARP Notarios Titulos Enviados a la Sunarp page and returns it.
        """
        return SunarpTitulosEnviados(self.browser_ctx, self.TITULOS_ENVIADOS_URL)

    def go_to_titulos_observados(self) -> SunarpTitulosObservados:
        """
        Redirect to the SUNARP Notarios Titulos Observados page and returns it.
        """
        return SunarpTitulosObservados(self.browser_ctx, self.TITULOS_OBSERVADOS_URL)
