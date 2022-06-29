# Generated by Django 3.2.6 on 2021-12-08 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
        ('order', '0016_returnitem_returned_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderitem', verbose_name='Товар заказа'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='warehouse_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouseproduct', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='returnitem',
            name='warehouse_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouseproduct', verbose_name='Товар'),
        ),
    ]
