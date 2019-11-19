from django.test import TestCase
import os
import pep8


def walk_dir(dir: str=None):
    python_files = set()
    for root, dirs, files in os.walk(dir):
        for f in files:
            if os.path.isfile(os.path.join(root, f)):
                if f.endswith('.py'):
                    python_files.add(os.path.join(root, f))
    return python_files


class TestPep8(TestCase):

    def test_pep8(self):
        style = pep8.StyleGuide()
        style.options.ignore += ('E501',)
        errors = 0
        files = set()
        
        for directory in ['lab', 'prod2app']:
            files.update(walk_dir(directory))

        errors += style.check_files(files).total_errors

        self.assertEqual(errors, 0, 'PEP8 style errors: {}'.format(errors))