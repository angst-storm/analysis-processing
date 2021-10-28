from django import forms
from django.core.validators import FileExtensionValidator


class BloodTestForm(forms.Form):
    user = forms.CharField(required=False)
    pdf_file = forms.FileField(required=True, validators=[FileExtensionValidator(['pdf'])])
