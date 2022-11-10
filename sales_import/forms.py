import mimetypes

from django.forms import forms


class FileImportForm(forms.Form):
    file = forms.FileField(help_text='Only text file is accepted.', required=True)

    def clean_file(self):
        valid_content_types = ['text/plain']

        uploaded_file = self.cleaned_data['file']

        file_mime_type = mimetypes.guess_type(uploaded_file.name)[0]

        if file_mime_type not in valid_content_types:
            raise forms.ValidationError('Invalid file format!', code='invalid')

        return uploaded_file
