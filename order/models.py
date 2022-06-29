import os

from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail

from order.choices import ORDER_STATUS_CHOICES, INVOICE_STATUS_CHOICES, RETURN_ITEM_STATUS_CHOICES, \
    RETAIL_ORDER_STATUS_CHOICES


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создание')
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    agent = models.ForeignKey('user.Agent', on_delete=models.PROTECT,
                              verbose_name='Агент',
                              null=True, blank=True)
    counter_party = models.ForeignKey('counter_party.CounterParty',
                                      on_delete=models.PROTECT,
                                      verbose_name='Контрагент')
    status = models.CharField(max_length=255,
                              verbose_name='Статус',
                              choices=ORDER_STATUS_CHOICES)
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма заказа')
    comment = models.CharField(max_length=5000, null=True, blank=True,
                               verbose_name='Комментарий')
    delivered_at = models.DateTimeField(verbose_name='Время доставки', null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.created}"


class OrderItem(models.Model):
    order = models.ForeignKey('order.Order',
                              on_delete=models.PROTECT,
                              related_name='order_items',
                              verbose_name='Заказ')
    warehouse_product = models.ForeignKey('warehouse.WarehouseProduct',
                                          on_delete=models.CASCADE,
                                          verbose_name='Товар')
    count = models.FloatField(default=0,
                              verbose_name='Количество')
    price = models.IntegerField(default=0,
                                verbose_name='Цена')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма')
    item_type = models.BooleanField(verbose_name='Бонусная', default=False)

    def __str__(self):
        return f"{self.order_id} | {self.warehouse_product}"


class RetailOrder(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создание')
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    client = models.ForeignKey('counter_party.RetailClient',
                               on_delete=models.CASCADE,
                               related_name='retail_orders',
                               verbose_name='Клиент')
    status = models.CharField(max_length=255,
                              verbose_name='Статус',
                              choices=RETAIL_ORDER_STATUS_CHOICES)
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма заказа')

    def __str__(self):
        return f"{self.id} | {self.created}"


class RetailOrderItem(models.Model):
    order = models.ForeignKey('order.RetailOrder',
                              on_delete=models.CASCADE,
                              related_name='retail_order_items',
                              verbose_name='Розничный заказ')
    warehouse_product = models.ForeignKey('warehouse.WarehouseProduct',
                                          on_delete=models.CASCADE,
                                          verbose_name='Товар')
    count = models.FloatField(default=0,
                              verbose_name='Количество')
    price = models.IntegerField(default=0,
                                verbose_name='Цена')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма')

    def __str__(self):
        return f"{self.order_id} | {self.warehouse_product}"


class ReturnItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    warehouse_product = models.ForeignKey('warehouse.WarehouseProduct',
                                          on_delete=models.PROTECT,
                                          verbose_name='Товар')
    counter_party = models.ForeignKey('counter_party.CounterParty',
                                      on_delete=models.SET_NULL,
                                      related_name='return_items',
                                      verbose_name='Клиент',
                                      null=True, blank=True)
    status = models.CharField(verbose_name='Статус', max_length=255,
                              choices=RETURN_ITEM_STATUS_CHOICES,
                              default='created')
    count = models.FloatField(default=0,
                              verbose_name='Количество')
    write_off_count = models.FloatField(default=0,
                                        verbose_name='Списание кол.')
    returned_count = models.FloatField(default=0,
                                       verbose_name='Количество возвращаемых товаров в склад')
    price = models.IntegerField(default=0,
                                verbose_name='Цена')
    total = models.BigIntegerField(default=0,
                                   verbose_name='Сумма')
    deliver = models.ForeignKey('user.Deliver',
                                on_delete=models.PROTECT,
                                verbose_name='Доставщик')

    def __str__(self):
        return f"{self.warehouse_product}"


class InvoiceProvider(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя поставщика")
    address = models.CharField(max_length=500, verbose_name="Адрес поставщика")
    phone_number = models.CharField(max_length=255, verbose_name="Телефон поставщика")
    logo = models.ImageField(upload_to="invoice_provider_logo", verbose_name="Логотип Поставщика")

    def __str__(self):
        return f"{self.name} | {self.address} | {self.phone_number}"


class Invoice(models.Model):
    order = models.ForeignKey('Order', verbose_name='Заказ', on_delete=models.PROTECT)
    invoice_provider = models.ForeignKey('InvoiceProvider',
                                         verbose_name="Поставщик",
                                         null=True, blank=True,
                                         on_delete=models.PROTECT)
    user = models.ForeignKey('user.User', verbose_name='Пользователь', on_delete=models.PROTECT)
    deliver = models.ForeignKey('user.Deliver', on_delete=models.PROTECT,
                                verbose_name='Доставщик',
                                null=True, blank=True)
    status = models.CharField(verbose_name='Статус', choices=INVOICE_STATUS_CHOICES,
                              default='created', max_length=255)
    discount = models.IntegerField(verbose_name='Скидка', default=0)
    total = models.IntegerField(verbose_name='Сумма со скидкой', default=0)
    photo = models.ImageField(verbose_name='Фотография накладного', blank=True, null=True, editable=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.order.counter_party.full_name} | {self.total}"

    def save(self, *args, **kwargs):
        if self.photo:
            old_path = self.photo.path
            self.photo = get_thumbnail(self.photo, '2000x2000', quality=60, format='JPEG', ).name
            os.remove(old_path)
        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    INVOICE_ITEM_TYPE = (
        ('simple', 'Простой'),
        ('bonus', 'Бонусная'),
        ('discount', 'Скидочная'),
    )
    invoice = models.ForeignKey('Invoice', verbose_name='Накладная',
                                related_name='invoice_items',
                                on_delete=models.PROTECT)
    order_item = models.ForeignKey('OrderItem', verbose_name='Товар заказа', on_delete=models.PROTECT)
    count = models.FloatField(verbose_name='Количество', default=0)
    total_without_discount = models.IntegerField(verbose_name='Сумма', default=0)
    total = models.IntegerField(verbose_name='Сумма со скидкой', default=0)
    item_type = models.CharField(verbose_name='Тпи элемента', max_length=255,
                                 choices=INVOICE_ITEM_TYPE, default='simple')

    def __str__(self):
        return f"{self.order_item.warehouse_product.product.title} | {self.invoice_id}"
