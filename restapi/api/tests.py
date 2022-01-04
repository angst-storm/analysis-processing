import os
import json
from django.test import TestCase
from django.core.files import File
from .models import BloodTest


class BloodTestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BloodTest.objects.create(client_ip='127.0.0.1',
                                 client_file=File(open('parsers/testfiles/test.pdf', 'rb'), 'test.pdf'))
        BloodTest.objects.create(client_ip='127.0.0.1',
                                 client_file=File(open('parsers/testfiles/test.pdf', 'rb'), 'test.pdf'))

    @classmethod
    def tearDownClass(cls):
        BloodTest.objects.get(id=1).remove_file()
        super(BloodTestModelTest, cls).tearDownClass()

    def test_labels(self):
        fields_labels = {'client_ip': 'client ip',
                         'submit': 'submit',
                         'client_file': 'client file',
                         'parsing_completed': 'parsing completed',
                         'parsing_result': 'parsing result'}
        blood_test = BloodTest.objects.get(id=1)
        for field in fields_labels:
            label = blood_test._meta.get_field(field).verbose_name
            self.assertEquals(label, fields_labels[field])

    def test_client_ip_max_length(self):
        blood_test = BloodTest.objects.get(id=1)
        max_length = blood_test._meta.get_field('client_ip').max_length
        self.assertEquals(max_length, 45)

    def test_parsing_completed_default(self):
        blood_test = BloodTest.objects.get(id=1)
        self.assertEquals(blood_test.parsing_completed, False)

    def test_parsing_result_default(self):
        blood_test = BloodTest.objects.get(id=1)
        self.assertEquals(blood_test.parsing_result, 'no result')

    def test_client_file_download(self):
        blood_test = BloodTest.objects.get(id=1)
        self.assertTrue(os.path.exists(str(blood_test.client_file)))

    def test_parsing(self):
        blood_test = BloodTest.objects.get(id=1)
        self.assertFalse(blood_test.parsing_completed)
        self.assertEquals(blood_test.parsing_result, 'no result')
        blood_test.launch_parsing()
        self.assertTrue(blood_test.parsing_completed)
        if bool(os.environ.get('NON_GAG', False)):
            self.assertNotEquals(blood_test.parsing_result, 'no result')
        else:
            self.assertEquals(blood_test.parsing_result, 'Excellent!')

    def test_string_view(self):
        for test in BloodTest.objects.all():
            self.assertEquals(str(test),
                              f'BloodTest (ID={test.id}, IP={test.client_ip}, parsed={test.parsing_completed})')

    def test_file_remove(self):
        blood_test = BloodTest.objects.get(id=2)
        self.assertTrue(os.path.exists(str(blood_test.client_file)))
        blood_test.remove_file()
        self.assertFalse(os.path.exists(str(blood_test.client_file)))


class ViewTest(TestCase):
    tests_count = 10
    test_fields = ['id', 'client_ip', 'submit', 'client_file', 'parsing_completed', 'parsing_result']

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.tests_count):
            BloodTest.objects.create(client_ip='127.0.0.1',
                                     client_file=File(open('parsers/testfiles/test.pdf', 'rb'), 'test.pdf'))

    @classmethod
    def tearDownClass(cls):
        for blood_test in BloodTest.objects.all()[:cls.tests_count]:
            blood_test.remove_file()
        super(ViewTest, cls).tearDownClass()

    def test_blood_tests_list_get(self):
        resp = self.client.get('/blood-tests/')
        self.assertEquals(resp.status_code, 200)
        tests = json.loads(*resp)
        self.assertEquals(len(tests), self.tests_count)
        for test in tests:
            self.assertEquals(list(iter(test)), self.test_fields)

    def test_blood_test_detail_get(self):
        resp = self.client.get('/blood-tests/1/')
        self.assertEquals(resp.status_code, 200)
        test = json.loads(*resp)
        self.assertEquals(list(iter(test)), self.test_fields)

    def test_blood_test_detail_post(self):
        resp = self.client.post('/', {'client_file': open('parsers/testfiles/test.pdf', 'rb')})
        self.assertEquals(resp.status_code, 200)
        test = json.loads(*resp)
        self.assertEquals(list(iter(test)), self.test_fields)
        self.assertTrue(test['parsing_completed'])

    def test_blood_test_detail_post_without_file(self):
        resp = self.client.post('/')
        self.assertEquals(resp.status_code, 400)

    def test_blood_test_detail_post_validate(self):
        for file in ['test.pdf', 'test.png', 'test.jpg']:
            resp = self.client.post('/', {'client_file': open(f'parsers/testfiles/{file}', 'rb')})
            self.assertEquals(resp.status_code, 200)
        for file in ['test.some']:
            resp = self.client.post('/', {'client_file': open(f'parsers/testfiles/{file}', 'rb')})
            self.assertEquals(resp.status_code, 400)

    def test_blood_test_detail_post_without_table(self):
        pass

    def test_main_page_get(self):
        resp = self.client.get('/')
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'form.html')

    def test_widget_get(self):
        resp = self.client.get('/static/widget.js')
        self.assertEquals(resp.status_code, 200)
