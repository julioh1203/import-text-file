from django.test import TestCase

from sales_import.models import Sale


class SaleModelTest(TestCase):

    def create_sale(self):
        return Sale.objects.create(buyer='João Silva', description='R$10 off R$20 of food',
                                   unit_price=10.0, amount=2, address='987 Fake St',
                                   supplier="Bob's Pizza")

    def test_save_sale(self):
        sale = self.create_sale()
        self.assertTrue(isinstance(sale, Sale))
        self.assertEqual(Sale.objects.all().count(), 1)
