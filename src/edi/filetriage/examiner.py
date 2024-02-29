from messages import get_error_result, get_msg_result

from pdfid import pdfid

import tempfile
import os
import json
import subprocess


def examine_pdf(file_object):
    counts = get_pdf_counts(file_object)
    if counts is None:
        return get_error_result('examine_pdf_unknown')

    pages = counts['pages']
    scripts = counts['scripts']
    executes = counts['executes']
    acroforms = counts['acroforms']
    filters = counts['filters']

    if counts['obj_streams'] > 0:
        sub_obj_content = subprocess.run(['pdf-parser.py', '-s', 'objstm', '-f', counts['tmp_file_name']], stdout=subprocess.PIPE).stdout
        sub_counts = get_pdf_counts(sub_obj_content, no_read=True)
        os.unlink(counts['tmp_file_name'])
        if sub_counts is None:
            return get_error_result('examine_pdf_unknown')
        os.unlink(sub_counts['tmp_file_name'])

        scripts += sub_counts['scripts']
        executes += sub_counts['executes']
        acroforms += sub_counts['acroforms']
        filters += sub_counts['filters']

    if scripts > 0:
        if executes > 0 or acroforms > 0 or filters > 0:
            if pages <= 1:
                return get_msg_result('risk_high')
            else:
                return get_msg_result('risk_medium')
        else:
            return get_msg_result('risk_low')
    else:
        return get_msg_result('risk_none')


def get_pdf_counts(file_object, no_read=False):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    if no_read:
        tmp_file.write(file_object)
    else:
        tmp_file.write(file_object.read())
    tmp_file.close()

    xml = pdfid.PDFiD(tmp_file.name)
    json_string = pdfid.PDFiD2JSON(xml, True)
    results = json.loads(json_string)

    pages = 0
    obj_streams = 0
    scripts = 0
    executes = 0
    acroforms = 0
    filters = 0

    for element in results:
        pdfid_element = element.get('pdfid')
        error_occured = pdfid_element.get('errorOccured')
        is_pdf = pdfid_element.get('isPdf')
        if error_occured != 'False' or is_pdf != 'True':
            os.unlink(tmp_file.name)
            return None

        for keyword in pdfid_element.get('keywords').get('keyword'):
            if keyword['name'] == '/Page':
                pages += keyword['count']
            elif keyword['name'] == '/ObjStm':
                obj_streams += keyword['count']
            elif keyword['name'] in ['/JS', '/JavaScript', '/RichMedia']:
                scripts += keyword['count']
            elif keyword['name'] in ['/AA', '/OpenAction', '/Launch']:
                executes += keyword['count']
            elif keyword['name'] == '/AcroForm':
                acroforms += keyword['count']
            elif keyword['name'] in ['/Colors > 2^24', '/JBIG2Decode']:
                filters += keyword['count']

    return {'pages': pages, 'obj_streams': obj_streams, 'scripts': scripts,
            'executes': executes, 'acroforms': acroforms, 'filters': filters,
            'tmp_file_name': tmp_file.name}
