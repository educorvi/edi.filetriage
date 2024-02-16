from types_helper import get_mime_type, get_method, check_appendix
from messages import get_error, get_msg
import examiner

import os


def check_file(file_object):
    # risk: low, medium, high, None

    # general checks

    # mimetype
    mimetype = get_mime_type(file_object)
    if mimetype is None:
        return {'success': False, 'risk': None, 'reason': 'unknown_mimetype', 'message': get_error('unknown_mimetype')}

    # appendix
    filename = os.path.basename(file_object.name)
    appendix_check_result = check_appendix(filename, mimetype)
    if appendix_check_result is None:
        return {'success': False, 'risk': None, 'reason': 'no_appendix', 'message': get_error('no_appendix')}
    if not appendix_check_result:
        return {'success': True, 'risk': 'high', 'reason': 'false_appendix', 'message': get_msg('false_appendix')}

    # examine method
    examine_method_string = get_method(mimetype)
    if examine_method_string is None:
        return {'success': False, 'risk': None, 'reason': 'no_examine_method', 'message': get_error('no_examine_method')}
    if examine_method_string == 'risk':
        return {'success': True, 'risk': 'high', 'reason': 'risky_mimetype', 'message': get_msg('risky_mimetype')}
    examine_method = getattr(examiner, examine_method_string, None)
    if examine_method is None:
        return {'success': False, 'risk': None, 'reason': 'no_examine_method', 'message': get_error('no_examine_method')}

    # call examine method
    examine_result = examine_method(file_object)
    return examine_result


if __name__ == '__main__':
    BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    test_file_names = [f for f in os.listdir(BASE_PATH)]
    test_file_paths = [os.path.join(BASE_PATH, test_file) for test_file in test_file_names]
    test_file_objects = [open(test_file_path, 'rb') for test_file_path in test_file_paths]

    for test_file_object in test_file_objects:
        print(check_file(test_file_object))

