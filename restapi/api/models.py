import os
from django.db import models
from django.utils import timezone
from parsers import tesseract_parser, gag_parser, narrow_parser
from transliterate import translit


def get_filename(instance, filename):
    return f'parsers/{translit(filename, "ru", reversed=True)}'


class BloodTest(models.Model):
    submit = models.DateTimeField(default=timezone.now)
    client_ip = models.CharField(max_length=45, default='unknown ip')
    client_file = models.FileField(upload_to=get_filename, default="")
    parsing_completed = models.BooleanField(default=False)
    table_found = models.BooleanField(default=False)
    table_formatted = models.BooleanField(default=False)
    laboratory = models.TextField(default='unknown')
    parsing_result = models.TextField(default='no result')

    def launch_parsing(self):
        if bool(os.environ.get('NON_GAG', False)):
            self.table_found, self.table_formatted, self.laboratory, self.parsing_result = \
                narrow_parser.parse(self.client_file.name)
        else:
            self.table_found, self.table_formatted, self.laboratory, self.parsing_result = \
                False, False, 'unknown', gag_parser.parse(self.client_file.name)
        self.parsing_completed = True

    def remove_file(self):
        os.remove(str(self.client_file))

    def __str__(self):
        return f'BloodTest (ID={self.id}, IP={self.client_ip}, parsed={self.parsing_completed})'
