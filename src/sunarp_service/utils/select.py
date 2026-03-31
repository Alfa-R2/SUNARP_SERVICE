from patchright.sync_api import FrameLocator, Locator, Page


def get_option_to_select(
    options: list[Locator], option_to_select_text: str
) -> Locator | None:
    return next(
        (
            option
            for option in options
            if (text_option := option.text_content())
            if text_option.strip() == option_to_select_text
        ),
        None,
    )


def click_select(page: Page, selector: str) -> None:
    select = page.locator(selector)
    select.click()
    page.wait_for_load_state(state="domcontentloaded")


def select_option(
    page_or_iframe: Page | FrameLocator, selector: str, option_text: str
) -> None:
    select = page_or_iframe.locator(selector)
    if not select.is_disabled():
        select.select_option(option_text)
