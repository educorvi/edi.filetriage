from types_helper import get_mime_type, get_method, check_appendix
from messages import get_error_result, get_msg_result
import examiner

import os


def check_file(file_object):
    # risk: none, low, medium, high
    # 0, 1, 2, 3

    # general checks

    # mimetype
    mimetype = get_mime_type(file_object)
    if mimetype is None:
        return get_error_result('unknown_mimetype')

    # appendix
    filename = os.path.basename(file_object.name)
    appendix_check_result = check_appendix(filename, mimetype)
    if appendix_check_result is None:
        return get_error_result('no_appendix')
    if not appendix_check_result:
        return get_msg_result('false_appendix')

    # examine method
    examine_method_string = get_method(mimetype)
    if examine_method_string is None:
        return get_error_result('no_examine_method')
    if examine_method_string == 'risk':
        return get_msg_result('risky_mimetype')
    examine_method = getattr(examiner, examine_method_string, None)
    if examine_method is None:
        return get_error_result('no_examine_method')

    # call examine method
    examine_result = examine_method(file_object)
    return examine_result


if __name__ == '__main__':
    BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    test_file_names = [f for f in os.listdir(BASE_PATH)]
    test_file_paths = [os.path.join(BASE_PATH, test_file) for test_file in test_file_names]
    test_file_objects = [open(test_file_path, 'rb') for test_file_path in test_file_paths]

    for test_file_object in test_file_objects:
        try:
            print({'file': test_file_object.name})
            print(check_file(test_file_object))
        except Exception as e:
            print({'error': e})

