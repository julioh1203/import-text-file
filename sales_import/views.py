import os

import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

from importation import settings
from sales_import.forms import FileImportForm
from .models import Sale
from .utils import handle_uploaded_file


def upload_file(request):
    if request.method == "POST":
        form = FileImportForm(request.POST, request.FILES)
        if form.is_valid():
            file_uploaded = request.FILES['file']
            handle_uploaded_file(file_uploaded)
            text_file = f'{settings.MEDIA_ROOT}/{file_uploaded}'

            df = pd.read_table(text_file, sep='\t')

            sale_instance = [
                Sale(
                    buyer=row['Comprador'],
                    description=row['Descrição'],
                    unit_price=row['Preço Unitário'],
                    amount=row['Quantidade'],
                    address=row['Endereço'],
                    supplier=row['Fornecedor']
                ) for index, row in df.iterrows()
            ]
            Sale.objects.bulk_create(sale_instance)

            os.remove(text_file)

            pd.set_option('colheader_justify', 'center')
            last_imported_saled = df.to_html(index=False)

            return render(request, 'sales_import/list_imports.html', {'last_imported_saled': last_imported_saled})
        else:
            return HttpResponse(request, form.errors)
    else:
        form = FileImportForm()
        return render(request, 'sales_import/upload.html', {'form': form})
