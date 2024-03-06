import os

from edi.filetriage.types_helper import get_mime_type, get_method, check_extension as check_extension_helper
from edi.filetriage.results import get_error_result, get_msg_result
from edi.filetriage import examiner


def check_extension(filename, mimetype):
    """Überprüft, ob die Dateiendung gültig für einen gegebenen Mimetype ist.
    :param filename: (str) Dateiname oder ganzer Pfad
    :param mimetype: (str) Mimetype der überprüft werden soll
    :return: (dict) {'valid': <None / True / False>, 'message': str}
    Falls ein Fehler auftritt: 'valid': None
    """
    return check_extension_helper(filename, mimetype)


def analyse_file(file_object, check_file_extension=True):
    """Untersucht ein Dateiobjekt auf bösartigen Inhalt
    :param file_object: Das Dateiobjekt (z.B. erzeugt mit open())
    :param check_file_extension: (bool) True, falls die Dateiendung auf Gültigkeit überprüft werden soll
    :return: {'success': <True / False>, 'risk': <None / 0 / 1 / 2 / 3>, 'mimetype': <mimetype>,
              'result': <result_string>, 'message': <readable Message>}
    'success': False falls ein Fehler auftritt (dann 'risk': None), sonst 'success': True und 'risk': 0..3
    'risk': (0) kein Risiko, (1) niedriges Risiko, (2) mittleres Risiko, (3) hohes Risiko
    'mimetype': ermittelter Mimetype der Datei
    'result': Kurzer String, der das Ergebnis der Prüfung beschreibt (siehe results.py)
    'message': Lange, lesbare Beschreibung des Risikos / des Fehlers
    """

    # general checks

    # mimetype
    mimetype = get_mime_type(file_object)
    if mimetype is None:
        return get_error_result('unknown_mimetype')

    # extension
    if check_file_extension:
        filename = os.path.basename(file_object.name)
        extension_check_result = check_extension(filename, mimetype)
        valid = extension_check_result.get('valid')
        if valid is None:
            return get_error_result('mimetype_no_extensions', mimetype)
        if not valid:
            return get_msg_result('false_appendix', mimetype)

    # examine method
    examine_method_string = get_method(mimetype)
    if examine_method_string is None:
        return get_error_result('no_examine_method', mimetype)
    if examine_method_string == 'risk':
        return get_msg_result('risky_mimetype', mimetype)
    examine_method = getattr(examiner, examine_method_string, None)
    if examine_method is None:
        return get_error_result('no_examine_method', mimetype)

    # call examine method
    examine_result = examine_method(file_object, mimetype)
    return examine_result


def analyse_file_list(file_object_list, check_file_extension=True, prints=False, merge_results=True, use_paths=False):
    """Untersucht ein Liste von Dateiobjekten auf bösartigen Inhalt
    :param file_object_list: List von Dateiobjekten (z.B. erzeugt mit open())
    :param check_file_extension: (bool) True, falls die Dateiendungen auf Gültigkeit überprüft werden sollen
    :param prints: (bool) True, falls der Fortschritt und Meldungen in der Konsole ausgegeben werden sollen
    :param merge_results: (bool) True, falls die Ergebnisse nach Risiko und Meldung gruppiert werden sollen
    :param use_paths: (bool) True, falls statt File-Objekten Pfade übergeben werden sollen
    """

    if merge_results:
        successful = [{'risk': 0, 'count': 0, 'results': []}, {'risk': 1, 'count': 0, 'results': []}, {'risk': 2, 'count': 0, 'results': []}, {'risk': 3, 'count': 0, 'results': []}]
        not_successful = []
        i = 0
        for file_object in file_object_list:
            i += 1
            if use_paths:
                file_object = open(file_object, 'rb')
            if prints: print(f'Analysiere Datei {i}: {file_object.name}')
            result = analyse_file(file_object, check_file_extension)
            if prints: print(f'Analyse von Datei {i} fertig: {result}')

            success = result['success']
            risk = result['risk']
            mimetype = result['mimetype']
            result_id = result['result']
            message = result['message']

            if not success:
                item_found = False
                for not_success_item in not_successful:
                    if not_success_item['result'] == result_id:
                        item_found = True
                        not_success_item['files'].append({'path': file_object.name, 'mimetype': mimetype})
                        not_success_item['count'] += 1
                        break
                if not item_found:
                    not_successful.append({'result': result_id, 'message': message, 'count': 1, 'files': [{'path': file_object.name, 'mimetype': mimetype}]})
            else:
                item_found = False
                risk_dict = successful[risk]
                result_list = risk_dict['results']
                risk_dict['count'] += 1
                for success_item in result_list:
                    if success_item['result'] == result_id:
                        item_found = True
                        success_item['files'].append({'path': file_object.name, 'mimetype': mimetype})
                        success_item['count'] += 1
                        break
                if not item_found:
                    result_list.append({'result': result_id, 'message': message, 'count': 1,
                                        'files': [{'path': file_object.name, 'mimetype': mimetype}]})

        return {'successful': successful, 'not_successful': not_successful}

    else:
        results = []
        i = 0
        for file_object in file_object_list:
            i += 1
            if use_paths:
                file_object = open(file_object, 'rb')
            if prints: print(f'Analysiere Datei {i}: {file_object.name}')
            result = analyse_file(file_object, check_file_extension)
            result['path'] = file_object.name
            results.append(result)
            if prints: print(f'Analyse von Datei {i} fertig: {result}')
        return results


def analyse_directory(absolute_path, recursive=True, check_file_extension=True, prints=False, merge_results=True):
    """Untersucht alle Dateien in einem Verzeichnis auf bösartigen Inhalt
    :param absolute_path: (str) Absoluter Pfad des Ordners
    :param recursive: (bool) Rekursiv in Unterverzeichnisse absteigen
    :param check_file_extension: (bool) True, falls die Dateiendungen auf Gültigkeit überprüft werden sollen
    :param prints: (bool) True, falls der Fortschritt und Meldungen in der Konsole ausgegeben werden sollen
    :param merge_results: (bool) True, falls die Ergebnisse nach Risiko und Meldung gruppiert werden sollen
    """
    if recursive:
        paths = [os.path.join(root, file) for root, _, files in os.walk(absolute_path) for file in files]
    else:
        paths = [os.path.join(absolute_path, file) for file in os.listdir(absolute_path)]
    return analyse_file_list(paths, check_file_extension, prints, merge_results, True)


if __name__ == '__main__':
    # Example usage
    folder = 'test_malicious_files'
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
    print(analyse_directory(path, recursive=True, check_file_extension=True, prints=True, merge_results=False))
