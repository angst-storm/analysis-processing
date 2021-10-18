from django.db import models
import os


def analyzes_path():
    directory_path = os.path.abspath(__file__)
    return directory_path[:directory_path.rfind('\\')] + '\\analyzes'


class PDFFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=analyzes_path())
