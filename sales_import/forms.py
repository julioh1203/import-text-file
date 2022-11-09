from django.core.exceptions import ValidationError
from django.forms import forms


def validate_file(file_uploaded):
    content_types = ['text/plain']
    if file_uploaded.content_type not in content_types:
        raise ValidationError('Invalid file format!')
    return file_uploaded


class FileImportForm(forms.Form):
    file = forms.FileField(help_text='Only text file is accepted.', required=True, validators=[validate_file])

    # validators=[FileTypeValidator(allowed_types=['text/plain'])])
