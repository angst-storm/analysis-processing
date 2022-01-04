from django import forms
from django.core.validators import FileExtensionValidator


class BloodTestForm(forms.Form):
    client_file = forms.FileField(required=True, validators=[FileExtensionValidator(['pdf', 'jpg', 'png'])])
