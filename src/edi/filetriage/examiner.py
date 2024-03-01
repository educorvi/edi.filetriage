import tempfile
import os
import json
import subprocess

from didier_stevens import pdfid
from results import get_error_result, get_msg_result

#import binwalk


def examine_pdf(file_object):
    counts = get_pdf_counts(file_object)
    if counts is None:
        return get_error_result('examine_pdf_unknown')

    pages = counts['pages']
    scripts = counts['scripts']
    actions = counts['actions']
    acroforms = counts['acroforms']
    filters = counts['filters']

    if counts['obj_streams'] > 0:
        pdf_parser_path = os.path.join(os.path.dirname(__file__), 'didier_stevens/pdf-parser.py')
        sub_obj_content = subprocess.run(['python3', pdf_parser_path, '-s', 'objstm', '-f', counts['tmp_file_name']], stdout=subprocess.PIPE).stdout
        sub_counts = get_pdf_counts(sub_obj_content, object_streams=True)
        os.unlink(counts['tmp_file_name'])
        if sub_counts is None:
            return get_error_result('examine_pdf_unknown')
        os.unlink(sub_counts['tmp_file_name'])

        pages += sub_counts['pages']
        scripts += sub_counts['scripts']
        actions += sub_counts['actions']
        acroforms += sub_counts['acroforms']
        filters += sub_counts['filters']

    if scripts > 0:
        if actions > 0 or acroforms > 0 or filters > 0:
            if pages <= 1:
                return get_msg_result('pdf_script_action_page')
            else:
                return get_msg_result('pdf_script_action')
        else:
            return get_msg_result('pdf_script')
    elif actions > 0:
        return get_msg_result('pdf_action')
    elif pages < 1:
        return get_msg_result('pdf_no_pages')
    else:
        return get_msg_result('risk_none')


def get_pdf_counts(file_object, object_streams=False):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    if object_streams:
        tmp_file.write(file_object)
    else:
        tmp_file.write(file_object.read())
    tmp_file.close()

    xml = pdfid.PDFiD(tmp_file.name, force=object_streams)
    json_string = pdfid.PDFiD2JSON(xml, True)
    results = json.loads(json_string)

    pages = 0
    obj_streams = 0
    scripts = 0
    actions = 0
    acroforms = 0
    filters = 0

    for element in results:
        pdfid_element = element.get('pdfid')
        error_occured = pdfid_element.get('errorOccured')
        is_pdf = pdfid_element.get('isPdf')
        if error_occured != 'False' or (is_pdf != 'True' and not object_streams):
            os.unlink(tmp_file.name)
            return None

        for keyword in pdfid_element.get('keywords').get('keyword'):
            if keyword['name'] == '/Page':
                pages += keyword['count']
            elif keyword['name'] == '/ObjStm':
                obj_streams += keyword['count']
            elif keyword['name'] in ['/JS', '/JavaScript', '/RichMedia']:
                scripts += keyword['count']
            elif keyword['name'] in ['/AA', '/OpenAction', '/Launch', '/Action']:
                actions += keyword['count']
            elif keyword['name'] == '/AcroForm':
                acroforms += keyword['count']
            elif keyword['name'] in ['/Colors > 2^24', '/JBIG2Decode']:
                filters += keyword['count']

    return {'pages': pages, 'obj_streams': obj_streams, 'scripts': scripts,
            'actions': actions, 'acroforms': acroforms, 'filters': filters,
            'tmp_file_name': tmp_file.name}


def examine_office(file_object):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(file_object.read())
    tmp_file.close()
    oledump_path = os.path.join(os.path.dirname(__file__), 'didier_stevens/oledump/oledump.py')
    obj_content = subprocess.run(['python3', oledump_path, '-j', tmp_file.name], stdout=subprocess.PIPE).stdout
    os.unlink(tmp_file.name)
    try:
        jsonresults = json.loads(obj_content)
    except:
        jsonresults = {}
    if jsonresults:
        for i in jsonresults['items']:
            if 'VBA' in i['name']:
                return get_msg_result('office_vba')
    return get_msg_result('risk_none')


"""
def examine_image(file_object):
    tmp_file = tempfile.NamedTemporaryFile(delete=False)
    tmp_file.write(file_object.read())
    tmp_file.close()
    import pdb; pdb.set_trace()
    for module in binwalk.scan(tmp_file.name, signature=True, extract=True):
        for result in module.results:
            if result.file.path in module.extractor.output:
                # These are files that binwalk carved out of the original firmware image, a la dd
                if result.offset in module.extractor.output[result.file.path].carved:
                    extractor_output = module.extractor.output[result.file.path].carved[result.offset]
                    print("Carved data from offset 0x%X to %s" % (result.offset, extractor_output))
                    # These are files/directories created by extraction utilities (gunzip, tar, unsquashfs, etc)
                if result.offset in module.extractor.output[result.file.path].extracted:
                    extractor_output = module.extractor.output[result.file.path].extracted[result.offset].files
                    extractor_command = module.extractor.output[result.file.path].extracted[result.offset].command
                    print("Extracted %d files from offset 0x%X to '%s' using '%s'" % (len(extractor_output),
                                                                                      result.offset,
                                                                                      extractor_output[0],
                                                                                      extractor_command))
    return {'level': 'warn', 'message': 'Die Datei konnte aufgrund eines Fehlers nicht geprüft werden'}
"""
