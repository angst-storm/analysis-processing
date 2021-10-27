from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BloodTest(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    user = models.CharField(max_length=80, default='unknown')
    submit = models.DateTimeField(default=timezone.now)
    pdf_file_name = models.CharField(max_length=80, default='not initialized')
    parsing_result = models.TextField(default='no result')
