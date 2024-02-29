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
    'risk_none': {'message': 'Die Datei stellt kein Sicherheitsrisiko dar', 'risk': 0},
    'risk_low': {'message': 'Die Datei stellt ein niedriges Sicherheitsrisiko dar', 'risk': 1},
    'risk_medium': {'message': 'Die Datei stellt ein mittleres Sicherheitsrisiko dar', 'risk': 2},
    'risk_high': {'message': 'Die Datei stellt ein hohes Sicherheitsrisiko dar', 'risk': 3},
    'pdf_script_action_page': {'message': 'Die Datei stellt ein hohes Sicherheitsrisiko dar: Es wurden ausführbare Skripte und auslösende Aktionen gefunden', 'risk': 3},
    'pdf_script_action': {'message': 'Die Datei stellt ein mittleres Sicherheitsrisiko dar: Es wurden ausführbare Skripte und auslösende Aktionen gefunden', 'risk': 2},
    'pdf_script': {'message': 'Die Datei stellt ein niedriges Sicherheitsrisiko dar: Es wurden ausführbare Skripte aber keine auslösenden Aktionen oder Ähnliches gefunden', 'risk': 1},
    'pdf_action': {'message': 'Die Datei stellt ein niedriges Sicherheitsrisiko dar: Es wurden Aktionen gefunden aber keine Skripte', 'risk': 1},
    'pdf_no_pages': {'message': 'Die Datei stellt ein hohes Sicherheitsrisiko dar: Sie enthält keine Seiten', 'risk': 3},

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
