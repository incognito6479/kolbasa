from django.db import models

from user.choices import REGIONS


class CounterParty(models.Model):
    full_name = models.CharField(max_length=255,
                                 verbose_name='ФИО контрагента')
    phone_number = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Номер телефона')
    address = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name='Адрес контрагента')
    region = models.CharField(max_length=255,
                              verbose_name='Область контрагента',
                              choices=REGIONS, null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name='Комментарии о контрагента')
    landmark = models.CharField(max_length=255, null=True, blank=True,
                                verbose_name='Оринтир')
    balance = models.IntegerField(default=0, verbose_name='Баланс контрагента')
    marker = models.CharField(max_length=255, null=True, blank=True,
                              verbose_name='Координаты маркера')

    def __str__(self):
        return f"{self.full_name} | {self.phone_number}"


class Provider(models.Model):
    full_name = models.CharField(max_length=255,
                                 verbose_name='Название поставщика')
    phone_number = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Номер телефона')
    address = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name='Адрес поставщика')
    content = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name='Комментарии о поставщике')
    balance = models.IntegerField(default=0, verbose_name='Баланс поставщика')

    def __str__(self):
        return f"{self.full_name} | {self.phone_number}"


class RetailClient(models.Model):
    full_name = models.CharField(max_length=255,
                                 verbose_name='Ф. И. О.')
    phone_number = models.CharField(max_length=255, null=True, blank=True,
                                    verbose_name='Номер телефона')
    address = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name='Адрес клиента')
    content = models.CharField(max_length=255, null=True, blank=True,
                               verbose_name='Комментарии о клиенте')
    balance = models.IntegerField(default=0, verbose_name='Баланс клиента')

    def __str__(self):
        return f"{self.full_name} | {self.phone_number} | {self.balance}"
