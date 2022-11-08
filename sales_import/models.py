from django.db import models


class Sale(models.Model):
    buyer = models.CharField('Comprador', max_length=256, blank=False, null=True)
    description = models.CharField('Descricao', max_length=256, blank=False, null=True)
    unit_price = models.DecimalField('Preço Unitário', decimal_places=2, blank=False, null=True, max_digits=9)
    amount = models.DecimalField('Quantidade', decimal_places=1, blank=False, null=True, max_digits=9)
    address = models.CharField('Endereço', max_length=256, blank=False, null=True)
    supplier = models.CharField('Fornecedor', max_length=256, blank=False, null=True)

    class Meta:
        db_table = 'sales'
