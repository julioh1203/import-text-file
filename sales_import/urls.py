from django.urls import path

from sales_import.views import upload_file, report_all_sales

app_name = 'sales_import'

urlpatterns = [
    path('upload/', upload_file, name='upload'),
    path('sales_report/', report_all_sales, name='sales_report'),
]
