default_error = 'Ein unbekannter Fehler ist aufgetreten'

errors = {
    'unknown_mimetype': 'Mime-Type der Datei konnte nicht ermittelt werden',
    'no_examine_method': 'Für diesen Dateityp ist (noch) keine Methode zur Untersuchung / Überprüfung vorhanden',
    'no_appendix': 'Für diesen Dateityp konnte die Prüfung der Dateiendung nicht durchgeführt werden'
}

default_message = 'Standard-Nachricht'

messages = {
    'risky_mimetype': 'Der Dateityp wird generell als gefährlich eingestuft. Daher ist keine Methode zur genaueren Untersuchung vorhanden',
    'false_appendix': 'Der tatsächliche (ermittelte) Dateityp unterscheidet sich von dem, durch die Dateiendung vorgeschlagenen Typen',
}


def get_error(error_id):
    error_msg = errors.get(error_id)
    if error_msg is None:
        return default_error
    return error_msg


def get_msg(msg_id):
    msg = messages.get(msg_id)
    if msg is None:
        return default_message
    return msg
