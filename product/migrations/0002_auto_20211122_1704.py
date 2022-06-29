# Generated by Django 3.2.6 on 2021-11-22 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='show_price',
            field=models.IntegerField(default=0, verbose_name='Цена со скидкой'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_type',
            field=models.CharField(choices=[('kg', 'кг'), ('piece', 'шт')], max_length=255, verbose_name='Единица измерения'),
        ),
    ]
