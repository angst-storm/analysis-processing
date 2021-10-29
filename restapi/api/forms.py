from django import forms
from django.core.validators import FileExtensionValidator


class BloodTestForm(forms.Form):
    pdf_file = forms.FileField(required=True, validators=[FileExtensionValidator(['pdf'])])
