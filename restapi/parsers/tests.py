import pandas as pd
from django.test import TestCase
from .pixel_scanner import get_scan_result
from .table_formatter import format_table
from .narrow_parser import tabula_parse
from .table_optimizer import optimize_table


class PixelScanTest(TestCase):
    def test_ugmk(self):
        self.assertEquals(get_scan_result('parsers/testfiles/ugmk/converted/page_0.png'), 'УГМК')

    def test_citilab(self):
        self.assertEquals(get_scan_result('parsers/testfiles/citilab/converted/page_0.png'), 'Ситилаб')

    def test_invitro(self):
        self.assertEquals(get_scan_result('parsers/testfiles/invitro/converted/page_0.png'), 'INVITRO')

    def test_kdl(self):
        self.assertEquals(get_scan_result('parsers/testfiles/kdl/converted/page_0.png'), 'KDL')

    def test_gemotest(self):
        self.assertEquals(get_scan_result('parsers/testfiles/gemotest/converted/page_0.png'), 'Гемотест')


class FormatterTest(TestCase):
    def lab_test(self, test_file_path, lab, expected_path):
        with open(expected_path, encoding='utf-8') as expected:
            test_file = format_table(pd.read_csv(test_file_path, encoding='utf-8'), lab)
            expected = expected.read()

            for t, e in zip(test_file.split('\r\n'), expected.split('\n')):
                self.assertEquals(t, e)

    def test_ugmk(self):
        self.lab_test('parsers/testfiles/ugmk/parsed.csv', 'УГМК', 'parsers/testfiles/ugmk/formatted.csv')

    def test_citilab(self):
        self.lab_test('parsers/testfiles/citilab/parsed.csv', 'Ситилаб', 'parsers/testfiles/citilab/formatted.csv')

    def test_invitro(self):
        self.lab_test('parsers/testfiles/invitro/parsed.csv', 'INVITRO', 'parsers/testfiles/invitro/formatted.csv')

    def test_kdl(self):
        self.lab_test('parsers/testfiles/kdl/parsed.csv', 'KDL', 'parsers/testfiles/kdl/formatted.csv')

    def test_gemotest(self):
        self.lab_test('parsers/testfiles/gemotest/parsed.csv', 'Гемотест', 'parsers/testfiles/gemotest/formatted.csv')


class TabulaParserTest(TestCase):
    def parse(self, test_file_path, lab, expected_path):
        with open(expected_path, encoding='utf-8') as expected:
            test_file = format_table(optimize_table(tabula_parse(test_file_path, lab), lab), lab).split('\r\n')
            expected = expected.read().split('\n')

            for t, e in zip(test_file, expected):
                self.assertEquals(t, e)

    def test_ugmk(self):
        self.parse('parsers/testfiles/ugmk/initial.pdf', 'УГМК', 'parsers/testfiles/ugmk/formatted.csv')

    def test_citilab(self):
        self.parse('parsers/testfiles/citilab/initial.pdf', 'Ситилаб', 'parsers/testfiles/citilab/formatted.csv')

    def test_invitro(self):
        self.parse('parsers/testfiles/invitro/initial.pdf', 'INVITRO', 'parsers/testfiles/invitro/formatted.csv')

    def test_gemotest(self):
        self.parse('parsers/testfiles/gemotest/initial.pdf', 'Гемотест', 'parsers/testfiles/gemotest/formatted.csv')
