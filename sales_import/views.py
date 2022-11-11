import os

import pandas as pd
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

            total_sales = df['Preço Unitário'].sum()

            pd.set_option('colheader_justify', 'left')
            last_imported_sales = df.to_html(index=False, classes="table table-striped", border=None)

            return render(request, 'sales_import/list_imports.html',
                          {'last_imported_sales': last_imported_sales, 'total_sales': total_sales})
        else:
            return HttpResponse(request, form.errors)
    else:
        form = FileImportForm()
        return render(request, 'sales_import/upload.html', {'form': form})


def report_all_sales(request):
    sales_qs = Sale.objects.all().values('buyer', 'description', 'unit_price', 'amount', 'address', 'supplier')

    table_columns = ['Comprador', 'Descrição', 'Preço Unitário', 'Quantidade', 'Endereço', 'Fornecedor']
    pd.set_option('colheader_justify', 'left')
    df = pd.DataFrame.from_records(sales_qs)
    df.columns = table_columns

    total_sales = df['Preço Unitário'].sum()

    sales = df.to_html(index=False, classes="table table-striped", border=None)
    return render(request, 'sales_import/report_all_sales.html', {'sales': sales, 'total_sales': total_sales})