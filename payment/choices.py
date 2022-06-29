OUTCAT_CHOICES = (
    ('order', 'Заказ'),
    ('retail_order', 'Розничный заказ'),
    ('income', 'Приход'),
    ('outlay', 'Расход'),
    ('counter_party', 'Контрагент'),
    ('movement', 'Перемещение'),
    ('user', 'Сотрудники'),
)


PAYMENT_TYPE_CHOICES = (
    ('outcome', 'Расход'),
    ('income', 'Приход'),
)

PAYMENT_METHOD_CHOICES = (
    ('cash', 'Наличные'),
    ('bank', 'Перечисление'),
    ('card', 'Картой'),
)

PAYMENT_STATUS_CHOICES = (
    ('created', 'Создано'),
    ('accepted', 'Принято'),
    ('rejected', 'Отказено'),
)
