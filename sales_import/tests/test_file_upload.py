import csv
import os

from django.test import TestCase, Client

from sales_import.forms import FileImportForm
from sales_import.models import Sale


class FileImportFormTest(TestCase):
    def setUp(self) -> None:
        self.form = FileImportForm()
        self.client = Client()

    def create_text_file_correct_format(self):
        self.text_file = 'sales.txt'
        with open(self.text_file, 'w+') as file:
            file.write("Comprador	Descrição	Preço Unitário	Quantidade	Endereço	Fornecedor\n")
            file.write("João Silva	R$10 off R$20 of food	10.0	2	987 Fake St	Bob's Pizza\n")
            file.write("Amy Pond	R$30 of awesome for R$10	10.0	5	456 Unreal Rd	Tom's Awesome Shop\n")
        return self.text_file

    def create_csv_file_for_test_wrong_format(self):
        self.csv_file = 'sales.csv'
        with open(self.csv_file, 'w+') as file:
            writer = csv.writer(file)
            writer.writerow("Comprador;Descrição;Preço Unitário;Quantidade;Endereço;Fornecedor \n")
            writer.writerow("João Silva;R$10 off R$20 of food;10.0;2;987 Fake St;Bob's Pizza \n")
        return self.csv_file

    def test_wrong_format(self):
        csv_file = self.create_csv_file_for_test_wrong_format()
        with open(csv_file, 'rb') as fp:
             self.client.post('/sales/upload/', {'file': fp})
        os.remove(csv_file)
        result = Sale.objects.all().count()
        self.assertEqual(result, 0)

    def test_correct_format(self):
        text_file = self.create_text_file_correct_format()
        with open(text_file, 'r') as fp:
            self.client.post('/sales/upload/', {'file': fp})
        os.remove(text_file)
        result = Sale.objects.values_list('buyer', flat=True)
        self.assertIn('João Silva', result)
        self.assertIn('Amy Pond', result)
