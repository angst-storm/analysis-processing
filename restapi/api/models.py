from django.db import models
from django.utils import timezone


class BloodTest(models.Model):
    client_ip = models.CharField(max_length=80, default='unknown ip')
    submit = models.DateTimeField(default=timezone.now)
    pdf_file = models.FileField(upload_to="parsers/", default="")
    parsing_completed = models.BooleanField(default=False)
    parsing_result = models.TextField(default='no result')
