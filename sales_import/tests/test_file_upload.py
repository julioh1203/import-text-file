import csv
import os

from django.test import TestCase

from sales_import.forms import FileImportForm


class FileImportFormTest(TestCase):
    def setUp(self) -> None:
        self.text_file = 'sales.txt'
        with open(self.text_file, 'w') as file:
            file.write("Comprador	Descrição	Preço Unitário	Quantidade	Endereço	Fornecedor \n")
            file.write("João Silva	R$10 off R$20 of food	10.0	2	987 Fake St	Bob's Pizza \n")

        self.form = FileImportForm()

    def create_csv_file_for_test_wrong_format(self):
        self.csv_file = 'sales.csv'
        with open(self.csv_file, 'w') as file:
            writer = csv.writer(file)
            writer.writerow("Comprador;Descrição;Preço Unitário;Quantidade;Endereço;Fornecedor \n")
            writer.writerow("João Silva;R$10 off R$20 of food;10.0;2;987 Fake St;Bob's Pizza \n")
        return self.csv_file

    def test_wrong_format(self):
        csv_file = self.create_csv_file_for_test_wrong_format()
        self.form.file = csv_file
        self.assertFalse(self.form.is_valid())

    def test_correct_format(self):
        self.form.file = self.text_file
        self.assertTrue(self.form.is_valid())

    def tearDown(self):
        # os.remove(self.text_file)
        os.remove(self.csv_file)
