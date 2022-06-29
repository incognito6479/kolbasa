# Generated by Django 3.2.6 on 2021-12-08 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_category'),
        ('income', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product', verbose_name='Товар'),
        ),
    ]