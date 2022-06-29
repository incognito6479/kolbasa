# Generated by Django 3.2.6 on 2021-12-13 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('counter_party', '0013_auto_20211213_1558'),
        ('warehouse', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0017_auto_20211208_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetailOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')),
                ('status', models.CharField(choices=[('created', 'В обработке'), ('completed', 'Завершен'), ('rejected', 'Отменен')], max_length=255, verbose_name='Статус')),
                ('total', models.BigIntegerField(default=0, verbose_name='Сумма заказа')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='counter_party.retailclient', verbose_name='Контрагент')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='RetailOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField(default=0, verbose_name='Количество')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('total', models.BigIntegerField(default=0, verbose_name='Сумма')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='retail_order_items', to='order.retailorder', verbose_name='Розничный заказ')),
                ('warehouse_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouseproduct', verbose_name='Товар')),
            ],
        ),
    ]
