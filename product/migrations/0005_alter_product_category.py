# Generated by Django 3.2.6 on 2021-12-08 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.productcategory', verbose_name='Категория Товара'),
        ),
    ]
