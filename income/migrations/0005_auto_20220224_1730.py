# Generated by Django 3.2.6 on 2022-02-24 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0004_auto_20211210_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomeitem',
            name='percent1',
            field=models.BigIntegerField(default=0, verbose_name='Процент 1'),
        ),
        migrations.AddField(
            model_name='incomeitem',
            name='percent2',
            field=models.BigIntegerField(default=0, verbose_name='Процент 2'),
        ),
        migrations.AddField(
            model_name='incomeitem',
            name='percent3',
            field=models.BigIntegerField(default=0, verbose_name='Процент 3'),
        ),
        migrations.AddField(
            model_name='incomeitem',
            name='percent4',
            field=models.BigIntegerField(default=0, verbose_name='Процент 4'),
        ),
    ]