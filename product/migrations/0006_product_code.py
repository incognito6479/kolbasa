# Generated by Django 3.2.6 on 2021-12-10 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(default='', max_length=255, verbose_name='Код'),
        ),
    ]
