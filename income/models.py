from django.db import models

from income.choices import INCOME_CHOICES


class Income(models.Model):
    warehouse = models.ForeignKey('warehouse.Warehouse',
                                  on_delete=models.PROTECT,
                                  verbose_name='Склад')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата прихода')
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    provider = models.ForeignKey('counter_party.Provider',
                                 on_delete=models.PROTECT,
                                 verbose_name='Поставщик')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма прихода')
    status = models.CharField(default='created', max_length=100,
                              verbose_name='Статус',
                              choices=INCOME_CHOICES)

    def __str__(self):
        return f"{self.id} | {self.created}"


class IncomeItem(models.Model):
    income = models.ForeignKey('income.Income',
                               on_delete=models.PROTECT,
                               verbose_name='Приход')
    product = models.ForeignKey('product.Product',
                                on_delete=models.PROTECT,
                                verbose_name='Товар')
    count = models.FloatField(default=0,
                              verbose_name='Количество')
    price = models.IntegerField(default=0,
                                verbose_name='Цена')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма')
    percent1 = models.BigIntegerField(default=0,
                                      verbose_name='Процент 1')
    percent2 = models.BigIntegerField(default=0,
                                      verbose_name='Процент 2')
    percent3 = models.BigIntegerField(default=0,
                                      verbose_name='Процент 3')
    percent4 = models.BigIntegerField(default=0,
                                      verbose_name='Процент 4')

    def __str__(self):
        return f"{self.income.id} | {self.product.title}"
