from patchright.sync_api import Dialog


def handle_alert(dialog: Dialog):
    print(f"Alerta detectada: {dialog.message} Tipo: {dialog.type}")
    dialog.accept()
