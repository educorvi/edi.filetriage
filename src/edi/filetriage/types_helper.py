import magic

from file_extensions import EXTENSIONS

methods = {
    # examine_pdf
    'application/pdf': 'examine_pdf',
    # examine office
    'application/msword': 'examine_office',
    'application/vnd.ms-excel': 'examine_office',
    'application/vnd.ms-powerpoint': 'examine_office',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'examine_office',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'examine_office',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'examine_office',
    # examine image TODO
    'image/jpeg': 'examine_image',
    'image/png': 'examine_image',
    'image/tiff': 'examine_image',
    'image/gif': 'examine_image',
    'image/bmp': 'examine_image',
    # examine text TODO
    'text/plain': 'examine_text',
    'text/rtf': 'examine_text',
    # risky types
    'application/octet-stream': 'risk',
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
        chunk = file_object.read(2048)
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
    mimetype_str = methods.get(mimetype)
    if mimetype_str is None:
        return None
    return mimetype_str


def check_extension(filename, mimetype):
    """
    Gibt zurück, ob die Dateiendung gültig für einen gegebenen Mimetype ist.
    """
    extension_list = EXTENSIONS.get(mimetype)
    if extension_list is None:
        return {'valid': None, 'message': 'Mimetype wurde nicht in der Liste gültiger Mimetypes gefunden'}
    if '.' not in filename:
        return {'valid': False, 'message': 'Der Dateiname enthält keine Dateiendung'}
    actual_extension = filename.split('.')[-1]
    if actual_extension not in extension_list:
        return {'valid': False, 'message': 'Die Dateiendung stimmt nicht mit dem Mimetype überein'}
    return {'valid': True, 'message': None}

