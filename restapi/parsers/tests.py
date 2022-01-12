from django.test import TestCase
from .pixelscan import get_scan_result
from .cropper import get_cropped_images
from .formatter import format_table


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


class CropperTest(TestCase):
    @staticmethod
    def crop_lab(lab, lab_dir, pages):
        for page in pages:
            get_cropped_images(lab, f'parsers/testfiles/{lab_dir}/converted/page_{page}.png')

    def test_ugmk(self):
        self.crop_lab('УГМК', 'ugmk', [0])
        self.assertTrue(True)

    def test_citilab(self):
        self.crop_lab('Ситилаб', 'citilab', [0, 1])
        self.assertTrue(True)

    def test_invitro(self):
        self.crop_lab('INVITRO', 'invitro', [0, 1])
        self.assertTrue(True)

    def test_kdl(self):
        self.crop_lab('KDL', 'kdl', [0, 1])
        self.assertTrue(True)

    def test_gemotest(self):
        self.crop_lab('Гемотест', 'gemotest', [0, 1])
        self.assertTrue(True)


class FormatterTest(TestCase):
    def lab_test(self, test_file_path, lab, expected_path):
        with open(test_file_path, encoding='utf-8') as test_file, open(expected_path, encoding='utf-8') as expected:
            test_file = format_table(lab, test_file.read())
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
