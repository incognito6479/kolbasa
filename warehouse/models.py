from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Название склада')

    address = models.CharField(max_length=255,
                               verbose_name='Адрес склада')

    def __str__(self):
        return self.name


class WarehouseProduct(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    warehouse = models.ForeignKey('warehouse.Warehouse',
                                  on_delete=models.PROTECT)
    product = models.ForeignKey('product.Product',
                                on_delete=models.PROTECT)
    count = models.FloatField(default=0)
    self_price = models.IntegerField(default=0)

    def __str__(self):
        return self.product.title
