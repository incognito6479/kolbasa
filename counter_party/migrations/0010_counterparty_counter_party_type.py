# Generated by Django 3.2.6 on 2021-12-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter_party', '0009_alter_counterparty_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='counterparty',
            name='counter_party_type',
            field=models.CharField(choices=[('client', 'Клиент'), ('provider', 'Поставщик')], default='client', max_length=255, verbose_name='Тип контрагента'),
        ),
    ]
