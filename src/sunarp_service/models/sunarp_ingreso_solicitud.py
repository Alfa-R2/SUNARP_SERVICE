from pathlib import Path

from patchright.sync_api import FrameLocator, Page

from sunarp_service.models.participants.participantes import (
    Favorecido,
    Otorgante,
    ParticipanteJuridico,
)
from sunarp_service.utils.alert import handle_alert
from sunarp_service.utils.select import click_select, select_option

from .types.actos_registrales import ActoRegistral
from .types.services import Service
from .types.solicitud import Solicitud


class SunarpIngresoSolicitud:
    """
    A class to interact with the SUNARP Notarios Ingreso Solicitud Inscripcion page.
    """

    def __init__(self, page: Page):
        self.page_ingreso_solicitud = page
        page.on("dialog", handle_alert)

    def __enter__(self) -> "SunarpIngresoSolicitud":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.page_ingreso_solicitud.is_closed():
            self.page_ingreso_solicitud.close()

    def __enter_option(self, option_to_select_text: str) -> None:
        input_select = self.page_ingreso_solicitud.locator(".select2-search__field")
        input_select.wait_for()
        self.page_ingreso_solicitud.wait_for_load_state(state="domcontentloaded")

        input_select.fill(option_to_select_text)
        input_select.press("Enter")

    def __select_service(self, service: Service) -> None:
        click_select(self.page_ingreso_solicitud, "#codActo + span")
        self.__enter_option(service)

    def __select_acto_registral(self, acto_registral: ActoRegistral) -> None:
        click_select(self.page_ingreso_solicitud, "#actoPoder + span")
        self.__enter_option(acto_registral)

    def __ingresar_solicitud(
        self,
        servicio: Service,
        acto_registral: ActoRegistral,
        oficina_registral: str,
        parte_notarial: str | Path,
        formulando_reserva: str = "",
        liquidacion: str = "",
        correo_ciudadano: str = "",
    ) -> None:
        self.page_ingreso_solicitud.click("a[href='#tab1']")

        self.__select_service(servicio)
        self.__select_acto_registral(acto_registral)
        select_option(self.page_ingreso_solicitud, "#codOficina", oficina_registral)
        self.page_ingreso_solicitud.set_input_files(
            "input[name='fileParte']", parte_notarial
        )
        self.page_ingreso_solicitud.fill("#formReserva", formulando_reserva)
        self.page_ingreso_solicitud.fill("#gRegistrales", liquidacion)
        self.page_ingreso_solicitud.fill("#correoElectronico", correo_ciudadano)
        self.page_ingreso_solicitud.click("#acepto")

    def __ingresar_participantes(
        self, participantes: list[Favorecido | Otorgante | ParticipanteJuridico]
    ) -> None:
        self.page_ingreso_solicitud.click("a[href='#tab2']")
        for participante in participantes:
            self.__ingresar_participante(participante)
        self.page_ingreso_solicitud.click("a[href='#tab1']")
        self.page_ingreso_solicitud.click("#acepto")

    def __ingresar_participante(
        self,
        data: Favorecido | Otorgante | ParticipanteJuridico,
    ) -> None:

        if isinstance(data, ParticipanteJuridico):
            iframe_form = self.__get_form_iframe("input[value='Participante Jurídico']")
            iframe_form.locator("#numRuc").fill(data.numero_ruc)
            iframe_form.locator("#partRegistral").fill(data.partida_registral)
            select_option(iframe_form, "#zonaRegistral", data.oficina_registral)
            iframe_form.locator("#btn-busqPartidaPJ").click()

            select_option(
                iframe_form,
                "#tipo_participante",
                data.tipo_participante,
            )
        else:
            iframe_form = self.__get_form_iframe("input[value='Participante Natural']")
            select_option(iframe_form, "#tipoDoc", data.tipo_documento)
            iframe_form.locator("#numDoc").fill(data.numero_documento)
            self.__handle_whether_participante_has_a_DNI_or_not(iframe_form, data)
            select_option(
                iframe_form,
                "#tipo_participante",
                data.tipo_participante,
            )
            if isinstance(data, Otorgante):
                select_option(iframe_form, "#profesion", data.ocupacion)
                select_option(iframe_form, "#nacionalidad", data.nacionalidad)
                select_option(iframe_form, "#estadoCiv", data.estado_civil)

        self.page_ingreso_solicitud.wait_for_timeout(2500)
        iframe_form.locator("#aceptar").click()

        self.page_ingreso_solicitud.evaluate(
            "selector => document.querySelector(selector)?.remove()",
            "dialog[style='center:yes;resizable:no;Width:550px;Height:520px;']",
        )

    def __get_form_iframe(self, activador_selector: str) -> FrameLocator:
        iframe_selector = "#dialog-body"

        button_form = self.page_ingreso_solicitud.locator(activador_selector)
        i_frame = self.page_ingreso_solicitud.locator(iframe_selector)

        button_form.wait_for()
        button_form.click()
        i_frame.wait_for()

        iframe_form = self.page_ingreso_solicitud.frame_locator(iframe_selector)

        return iframe_form

    def __handle_whether_participante_has_a_DNI_or_not(
        self,
        iframe_form: FrameLocator,
        participante: Otorgante | Favorecido,
    ) -> None:

        if participante.tipo_documento == "DNI DOCUMENTO NACIONAL DE IDENTIDAD":
            iframe_form.locator("#validar").click()
            return

        iframe_form.locator("#apaterno").fill(participante.primer_apellido)
        iframe_form.locator("#amaterno").fill(participante.segundo_apellido)
        iframe_form.locator("#nombres").fill(participante.pre_nombres)

    def __extraer_numero_solicitud(self) -> str:
        numero_solicitud_h3 = self.page_ingreso_solicitud.locator(
            "#seleccion :nth-child(3) td label"
        )
        numero_solicitud_h3.wait_for()
        return numero_solicitud_h3.inner_text()

    def ingresar_solicitud(self, solicitud: Solicitud) -> str:
        """
        Submit a solicitud to the SUNARP and return the number of Solicitud.

        Args:
            solicitud (Solicitud): Solicitud to submit.
        """

        self.__ingresar_solicitud(
            solicitud.servicio,
            solicitud.acto_registral,
            solicitud.oficina_registral,
            solicitud.parte_notarial,
            solicitud.formulando_reserva,
            solicitud.liquidacion,
            solicitud.correo_ciudadano,
        )

        self.__ingresar_participantes(solicitud.participantes)

        button_sign = self.page_ingreso_solicitud.locator("#enviar")
        button_sign.wait_for()
        button_sign.click()

        return self.__extraer_numero_solicitud()
