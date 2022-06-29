ORDER_STATUS_CHOICES = (
    ('created', 'В обработке'),
    ('accepted', 'Принято'),
    ('delivered', 'Доставлено'),
    ('completed', 'Завершен'),
    ('rejected', 'Отменен'),
)

RETAIL_ORDER_STATUS_CHOICES = (
    ('created', 'В обработке'),
    ('completed', 'Завершен'),
    ('rejected', 'Отменен'),
)

INVOICE_STATUS_CHOICES = (
    ('created', 'Создан'),
    ('during_delivery', 'В процессе доставки'),
    ('delivered', 'Доставлено'),
    ('rejected', 'Отменен'),
)

RETURN_ITEM_STATUS_CHOICES = (
    ('created', 'Создан'),
    ('acceptance', 'Принятие'),
    ('write-off', 'Списание'),
    ('rejected', 'Отменен'),
)
