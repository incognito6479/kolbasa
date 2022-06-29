from django.db import models
from .choices import MOVEMENT_CHOICES


class Movement(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата перемещение')
    user = models.ForeignKey('user.User', on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    from_warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT,
                                       verbose_name="Со склада", related_name='from_warehouse_movements')
    to_warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT,
                                     verbose_name="В склад", related_name='to_warehouse_movements')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма перемещение')
    status = models.CharField(default='created', max_length=100,
                              verbose_name='Статус',
                              choices=MOVEMENT_CHOICES)

    def __str__(self):
        return f"{self.id} | {self.created}"


class MovementItem(models.Model):
    movement = models.ForeignKey('movement.Movement', on_delete=models.PROTECT,
                                 verbose_name='Переход')
    warehouse_product = models.ForeignKey('warehouse.WarehouseProduct', on_delete=models.PROTECT,
                                          verbose_name='Товар')
    count = models.FloatField(default=0,
                              verbose_name='Количество')
    price = models.IntegerField(default=0,
                                verbose_name='Цена')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма')

    def __str__(self):
        return f"{self.movement.id} | {self.warehouse_product.product.title}"
