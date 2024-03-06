import unittest
import os
from src.edi.filetriage.checker import analyse_directory


class TestTriage(unittest.TestCase):

    def test_risk_files(self):
        expected = [
            {'name': 'test1.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test1bis.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test2.pdf', 'mimetype': 'application/pdf', 'risk': 3, 'result': 'pdf_no_pages'},
            {'name': 'test3.pdf', 'mimetype': 'application/pdf', 'risk': 3, 'result': 'pdf_script_action_page'},
            {'name': 'test4.pdf', 'mimetype': 'application/pdf', 'risk': 3, 'result': 'pdf_no_pages'},
            {'name': 'test5.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test6.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test7.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test8.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test9.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_action'},
            {'name': 'test10.pdf', 'mimetype': 'application/pdf', 'risk': 3, 'result': 'pdf_script_action_page'},
            {'name': 'test11.pdf', 'mimetype': 'application/pdf', 'risk': 1, 'result': 'pdf_script'},
        ]

        folder = 'risk_files'
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder)
        actual = analyse_directory(path, merge_results=False)

        for item in expected:
            item_path = os.path.join(path, item['name'])
            result = [a for a in actual if a['path'] == item_path]
            self.assertEqual(len(result), 1, f'did not get exactly one result for: {item}, got: {result}')
            result = result[0]
            self.assertEqual(result['success'], True, f'got error for: {item}, error: {result}')
            self.assertEqual(result['mimetype'], item['mimetype'], f'got wrong mimetype for: {item}, actual: {result}')
            self.assertEqual(result['risk'], item['risk'], f'got wrong risk for: {item}, actual: {result}')
            self.assertEqual(result['result'], item['result'], f'got wrong result_id for: {item}, actual: {result}')


if __name__ == '__main__':
    unittest.main()
