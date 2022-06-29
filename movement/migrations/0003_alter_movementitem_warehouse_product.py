# Generated by Django 3.2.6 on 2021-12-08 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
        ('movement', '0002_movement_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementitem',
            name='warehouse_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.warehouseproduct', verbose_name='Товар'),
        ),
    ]
