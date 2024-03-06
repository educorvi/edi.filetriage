default_error = 'Ein unbekannter Fehler ist aufgetreten'

errors = {
    'unknown_mimetype': 'Mime-Type der Datei konnte nicht ermittelt werden',
    'mimetype_no_extensions': 'Für diesen Mime-Type konnten keine gültigen Dateiendungen gefunden werden',
    'no_examine_method': 'Für diesen Dateityp ist (noch) keine Methode zur Untersuchung / Überprüfung vorhanden',
    'examine_pdf_unknown': 'Bei der Analyse des PDF-Dokuments gab es einen unbekannten Fehler',
}

messages = {
    'risky_mimetype': {'risk': 3, 'message': 'Der Dateityp wird generell als gefährlich eingestuft, der Inhalt wurde nicht weiter analysiert'},
    'false_appendix': {'risk': 3, 'message': 'Der tatsächliche (ermittelte) Dateityp unterscheidet sich von der Dateiendung oder der Dateiname enthält keine Dateiendung'},
    'risk_none': {'risk': 0, 'message': 'Im Rahmen der Analyse wurden keine Anhaltspunkte für ein Sicherheitsrisiko gefunden'},
    'pdf_script_action_page': {'risk': 3, 'message': 'Es wurden ausführbare Skripte und auslösende Aktionen gefunden und die Datei enthält nur eine Seite'},
    'pdf_script_action': {'risk': 2, 'message': 'Es wurden ausführbare Skripte und auslösende Aktionen gefunden'},
    'pdf_script': {'risk': 1, 'message': 'Es wurden ausführbare Skripte aber keine auslösenden Aktionen gefunden'},
    'pdf_action': {'risk': 1, 'message': 'Es wurden auslösende Aktionen gefunden aber keine Skripte'},
    'pdf_no_pages': {'risk': 3, 'message': 'Die Datei enthält keine Seiten'},
    'office_vba': {'risk': 3, 'message': 'Es wurden VBA Makros in der Datei gefunden'},
}

risk_messages = {
    '0': 'Die Datei stellt kein Sicherheitsrisiko dar',
    '1': 'Die Datei stellt ein niedriges Sicherheitsrisiko dar',
    '2': 'Die Datei stellt ein mittleres Sicherheitsrisiko dar',
    '3': 'Die Datei stellt ein hohes Sicherheitsrisiko dar',
}


def get_error_result(error_id, mimetype=None):
    error_msg = errors.get(error_id)
    if error_msg is None:
        error_id = 'default_error'
        error_msg = default_error
    return {'success': False, 'risk': None, 'mimetype': mimetype, 'result': error_id, 'message': error_msg}


def get_msg_result(msg_id, mimetype=None):
    msg = messages.get(msg_id)
    if msg is None:
        return get_error_result(None)
    risk = msg['risk']
    message = f'{risk_messages[str(risk)]}: {msg["message"]}'
    return {'success': True, 'risk': risk, 'mimetype': mimetype, 'result': msg_id, 'message': message}
