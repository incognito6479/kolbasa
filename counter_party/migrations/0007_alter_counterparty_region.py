# Generated by Django 3.2.6 on 2021-12-05 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter_party', '0006_alter_counterparty_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterparty',
            name='region',
            field=models.CharField(choices=[('bulungur', 'Булунгур'), ('ishtikhon', 'Иштихон'), ('jomboy', 'Джомбой'), ('paishanba', 'Пайшанба'), ('koshrabot', 'Кошработ'), ('oqtosh', 'Октош'), ('nurobod', 'Нуробод'), ('laish', 'Лаиш'), ('ziadin', 'Зиадин'), ('payariq', 'Паярик'), ('juma', 'Джума'), ('gulabad', 'Гулабад'), ('tayloq', 'Тойлок'), ('urgut', 'Ургут'), ('g_samaqand', 'г. Самарканд '), ('r_samaqand', 'р. Самарканд ')], max_length=255, verbose_name='Область контрагента'),
        ),
    ]