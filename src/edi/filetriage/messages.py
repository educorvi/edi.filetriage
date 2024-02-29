default_error = 'Ein unbekannter Fehler ist aufgetreten'

errors = {
    'unknown_mimetype': 'Mime-Type der Datei konnte nicht ermittelt werden',
    'no_examine_method': 'Für diesen Dateityp ist (noch) keine Methode zur Untersuchung / Überprüfung vorhanden',
    'no_appendix': 'Für diesen Dateityp konnte die Prüfung der Dateiendung nicht durchgeführt werden',
    'examine_pdf_unknown': 'Bei der Analyse des PDF-Dokuments gab es einen unbekannten Fehler',
}

messages = {
    'risky_mimetype': {'message': 'Der Dateityp wird generell als gefährlich eingestuft. Daher ist keine Methode zur genaueren Untersuchung vorhanden', 'risk': 3},
    'false_appendix': {'message': 'Der tatsächliche (ermittelte) Dateityp unterscheidet sich von dem, durch die Dateiendung vorgeschlagenen Typen', 'risk': 3},
    'risk_none': {'message': 'x', 'risk': 0},
    'risk_low': {'message': 'x', 'risk': 1},
    'risk_medium': {'message': 'x', 'risk': 2},
    'risk_high': {'message': 'x', 'risk': 3},
}


def get_error_result(error_id):
    error_msg = errors.get(error_id)
    if error_msg is None:
        error_id = 'default_error'
        error_msg = default_error
    return {'success': False, 'risk': None, 'reason': error_id, 'message': error_msg}


def get_msg_result(msg_id):
    msg = messages.get(msg_id)
    if msg is None:
        return get_error_result(None)
    return {'success': True, 'risk': msg['risk'], 'reason': msg_id, 'message': msg['message']}
