from django import forms


class BloodTestForm(forms.Form):
    user = forms.CharField(required=False)
    pdf_file = forms.FileField()

