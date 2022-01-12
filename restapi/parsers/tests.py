from django.test import TestCase
from .formatter import format_table


class FormatterTest(TestCase):
    def lab_test(self, test_file_path, lab, expected_path):
        with open(test_file_path, encoding='utf-8') as test_file, open(expected_path, encoding='utf-8') as expected:
            test_file = format_table(lab, test_file.read())
            expected = expected.read()

            for t, e in zip(test_file.split('\r\n'), expected.split('\n')):
                self.assertEquals(t, e)

    def test_ugmk(self):
        self.lab_test('parsers/testfiles/ugmk/parsed.csv', 'УГМК', 'parsers/testfiles/ugmk/formatted.csv')

    def test_citylab(self):
        self.lab_test('parsers/testfiles/citylab/parsed.csv', 'Ситилаб', 'parsers/testfiles/citylab/formatted.csv')

    def test_invitro(self):
        self.lab_test('parsers/testfiles/invitro/parsed.csv', 'INVITRO', 'parsers/testfiles/invitro/formatted.csv')

    def test_kdl(self):
        self.lab_test('parsers/testfiles/kdl/parsed.csv', 'KDL', 'parsers/testfiles/kdl/formatted.csv')

    def test_hemotest(self):
        self.lab_test('parsers/testfiles/hemotest/parsed.csv', 'Гемотест', 'parsers/testfiles/hemotest/formatted.csv')
