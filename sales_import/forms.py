from django.forms import forms
from upload_validator import FileTypeValidator


class FileImportForm(forms.Form):
    file = forms.FileField(help_text='Only text file is accepted.', required=True,
                           validators=[FileTypeValidator(allowed_types=['text'])])
