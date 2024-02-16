import magic

mimetypes = {
    'application/pdf': {'method': 'examine_pdf', 'appendixes': ['pdf']},
    'application/octet-stream': {'method': 'risk'},
    'application/msword': {'method': 'examine_office', 'appendixes': ['doc']},
    'application/vnd.ms-excel': {'method': 'examine_office', 'appendixes': ['xls']},
    'application/vnd.ms-powerpoint': {'method': 'examine_office', 'appendixes': ['ppt']},
    'application/vnd.ms-outlook': {'method': 'risk'},  # TODO
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': {'method': 'examine_office', 'appendixes': ['docx']},
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': {'method': 'examine_office', 'appendixes': ['xlsx']},
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': {'method': 'examine_office', 'appendixes': ['pptx']},
    'image/jpeg': {'method': 'examine_image', 'appendixes': ['jpg', 'jpeg']},
    'image/png': {'method': 'examine_image', 'appendixes': ['png']},
    'image/tiff': {'method': 'examine_image', 'appendixes': ['tiff', 'tif']},
    'image/gif': {'method': 'examine_image', 'appendixes': ['gif']},
    'image/bmp': {'method': 'examine_image', 'appendixes': ['bmp']},
    'video/mp4': {'method': 'risk'},
    'video/x-ms-asf': {'method': 'risk'},  # TODO
    'message/rfc822': {'method': 'risk'},
    'text/plain': {'method': 'examine_text', 'appendixes': ['txt']},
    'text/rtf': {'method': 'examine_text', 'appendixes': ['rtf']}
}


def get_mime_type(file_object):
    """Get the MIME type of a file based on its file object.
    :param file_object: The file object (eg. created with open()).
    :return: (str or None) The MIME type of the file, or None if an error occurs.
    """
    if file_object is None:
        return None
    try:
        file_object.seek(0)
        chunk = file_object.read(1024)
        result = magic.from_buffer(chunk, mime=True)
        return result
    except Exception as e:
        return None
    finally:
        file_object.seek(0)


def get_method(mimetype):
    """
    Gibt die Untersuchungsmethode anhand des ermittelten Mimetypes zurück.
    """
    mimetype_dict = mimetypes.get(mimetype)
    if mimetype_dict is None:
        return None
    return mimetype_dict.get('method')


def check_appendix(filename, mimetype):
    """
    Gibt zurück, ob die Dateiendung gültig für einen gegebenen Mimetype ist.
    """
    mimetype_dict = mimetypes.get(mimetype)
    if mimetype_dict is None:
        return None
    appendixes = mimetype_dict.get('appendixes')
    if appendixes is None:
        return None
    actual_appendix = filename.split('.')[-1]
    return actual_appendix in appendixes



