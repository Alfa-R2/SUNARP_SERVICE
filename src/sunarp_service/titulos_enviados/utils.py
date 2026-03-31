from patchright.sync_api import Locator


def get_cell_texts(row: Locator) -> tuple[str, ...]:
    label: Locator = row.locator("> td > label")
    return tuple(label.all_inner_texts())
