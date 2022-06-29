from django.db import models

from payment.choices import OUTCAT_CHOICES, PAYMENT_TYPE_CHOICES, PAYMENT_METHOD_CHOICES, PAYMENT_STATUS_CHOICES


class PaymentLog(models.Model):
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создание')
    user = models.ForeignKey('user.User',
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    outcat = models.CharField(max_length=255,
                              choices=OUTCAT_CHOICES)
    model_id = models.IntegerField(default=-1)
    outlay = models.ForeignKey('payment.Outlay',
                               on_delete=models.PROTECT,
                               verbose_name='Причина')
    payment_type = models.CharField(max_length=255,
                                    choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=255,
                                      choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(verbose_name='Статус', choices=PAYMENT_STATUS_CHOICES,
                              max_length=255, default='created')
    amount = models.IntegerField(default=0,
                                 verbose_name='Сумма')

    def __str__(self):
        return f"{self.created} | {self.amount}"


class Outlay(models.Model):
    title = models.CharField(max_length=255,
                             verbose_name='Причина')
    outcat = models.CharField(max_length=255,
                              choices=OUTCAT_CHOICES)

    def __str__(self):
        return f"{self.title} | {self.get_outcat_display()}"


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ProjectSetting(SingletonModel):
    cashier = models.IntegerField(default=0)

    def __str__(self):
        return str(self.cashier)

    class Meta:
        verbose_name = 'Касса'
        verbose_name_plural = 'Касса'