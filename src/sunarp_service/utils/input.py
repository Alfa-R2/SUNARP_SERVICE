from playwright.sync_api import Page


def wait_input_be_filled(page: Page, selector: str):
    page.wait_for_function(
        f"""() => document.querySelector("{selector}").value.trim() !== ''"""
    )
