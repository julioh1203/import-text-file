import csv
import os
from decimal import Decimal

from django.test import TestCase, Client

from sales_import.forms import FileImportForm
from sales_import.models import Sale


class TestSalesReport(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        Sale.objects.create(buyer='Amy Pond', description='R$30 of awesome for R$10', unit_price=20,
                            amount=10.0, address='456 Unreal Rd', supplier="Tom's Awesome Shop")

    def test_get_sales_report(self):
        response = self.client.get('/sales/sales_report/')
        html = response.content.decode('utf-8')
        self.assertIn('<td>Amy Pond</td>', html)
        self.assertIn('<td>20.00</td>', html)
