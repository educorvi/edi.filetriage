import os

from types_helper import get_mime_type, get_method, check_extension as check_extension_helper
from results import get_error_result, get_msg_result
import examiner


def check_extension(filename, mimetype):
    """Überprüft, ob die Dateiendung gültig für einen gegebenen Mimetype ist.
    :param filename: (str) Dateiname oder ganzer Pfad
    :param mimetype: (str) Mimetype der überprüft werden soll
    :return: (dict) {'valid': <None / True / False>, 'message': str}
    Falls ein Fehler auftritt: 'valid': None
    """
    return check_extension_helper(filename, mimetype)


def analyse_file(file_object, check_file_extension=False):
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
    examine_result = examine_method(file_object)
    return examine_result


def analyse_file_list(file_object_list, check_file_extension=False, prints=False):
    """Untersucht ein Liste von Dateiobjekten auf bösartigen Inhalt
    :param file_object_list: List von Dateiobjekten (z.B. erzeugt mit open())
    :param check_file_extension: (bool) True, falls die Dateiendungen auf Gültigkeit überprüft werden sollen
    :return: {'success': <True / False>, 'risk': <None / 0 / 1 / 2 / 3>, 'mimetype': <mimetype>,
              'result': <result_string>, 'message': <readable Message>}
    'success': False falls ein Fehler auftritt (dann 'risk': None), sonst 'success': True und 'risk': 0..3
    'risk': (0) kein Risiko, (1) niedriges Risiko, (2) mittleres Risiko, (3) hohes Risiko
    'mimetype': ermittelter Mimetype der Datei
    'result': Kurzer String, der das Ergebnis der Prüfung beschreibt (siehe results.py)
    'message': Lange, lesbare Beschreibung des Risikos / des Fehlers
    """

    successful = []
    not_successful = []
    i = 0
    for file_object in file_object_list:
        i += 1
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
                    not_success_item['files'].append({'name': file_object.name, 'mimetype': mimetype})
                    not_success_item['count'] += 1
                    break
            if not item_found:
                not_successful.append({'result': result_id, 'message': message, 'count': 0, 'files': [{'name': file_object.name, 'mimetype': mimetype}]})
        else:
            item_found = False
            result_found = False
            for success_item in successful:
                if success_item['risk'] == risk:
                    for result_item in success_item['results']:
                        if result_item['result'] == result_id:
                            result_found = True
                            result_item['files'].append({'name': file_object.name, 'mimetype': mimetype})
                            result_item['count'] += 1
                            break
                    if not result_found:
                        success_item['results'].append({'result': result_id, 'message': message, 'count': 0, 'files': [{'name': file_object.name, 'mimetype': mimetype}]})
                    else:
                        item_found = True
                        break
            if not item_found:
                result_item = {'result': result_id, 'message': message, 'count': 1, 'files': [{'name': file_object.name, 'mimetype': mimetype}]}
                successful.append({'risk': risk, 'results': [result_item]})

    return {'successful': successful, 'not_successful': not_successful}


if __name__ == '__main__':
    #TEST_FOLDER = 'test_non_malicious'
    TEST_FOLDER = 'test_good_all_mac'
    #TEST_FOLDER = 'test_office'
    BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEST_FOLDER)
    test_file_names = [f for f in os.listdir(BASE_PATH)]
    test_file_paths = [os.path.join(BASE_PATH, test_file) for test_file in test_file_names]
    test_file_objects = [open(test_file_path, 'rb') for test_file_path in test_file_paths]

    print(analyse_file_list(test_file_objects, True, True))

    """
    results = {}
    errors = []
    i = 1
    for test_file_object in test_file_objects:
        try:
            print(f'Analysing file {i}: {test_file_object.name}')
            #print({'file': test_file_object.name})
            result = analyse_file(test_file_object)
            print(f'Analysing finished: {result}')
            reason = result['reason']
            if results.get(reason) is None:
                result['files'] = []
                result['count'] = 0
                results[reason] = result
            results[reason]['files'].append(test_file_object.name)
            results[reason]['count'] += 1
        except Exception as e:
            print({'error': e})
            errors.append((e, test_file_object.name))
        finally:
            i += 1

    print('\nERRORS:\n')
    print(errors)
    print('\nRESULTS:\n')
    print(results)
    """
