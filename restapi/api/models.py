from django.db import models
from django.utils import timezone
from parsers import main_parser, gag_parser
import os


class BloodTest(models.Model):
    submit = models.DateTimeField(default=timezone.now)
    client_ip = models.CharField(max_length=45, default='unknown ip')
    client_file = models.FileField(upload_to="parsers/", default="")
    parsing_completed = models.BooleanField(default=False)
    table_found = models.BooleanField(default=False)
    parsing_result = models.TextField(default='no result')

    def launch_parsing(self):
        try:
            self.parsing_result = (main_parser if bool(os.environ.get('NON_GAG', False)) else gag_parser).parse(self.client_file.name)
        except ValueError:
            self.table_found = False
        else:
            self.table_found = True
        finally:
            self.parsing_completed = True

    def remove_file(self):
        os.remove(str(self.client_file))

    def __str__(self):
        return f'BloodTest (ID={self.id}, IP={self.client_ip}, parsed={self.parsing_completed})'
