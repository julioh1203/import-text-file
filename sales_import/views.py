from django.shortcuts import render

from sales_import.forms import FileImportForm


def upload_file(request):
    form = FileImportForm(request.POST, request.FILES)
    if form.is_valid():
        ...
    else:
        return form

