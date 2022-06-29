# Generated by Django 3.2.6 on 2021-12-04 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
        ('user', '0005_agent_deliver'),
        ('order', '0007_invoice_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='deliver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.deliver', verbose_name='Доставщик'),
        ),
        migrations.AddField(
            model_name='order',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.agent', verbose_name='Агент'),
        ),
        migrations.CreateModel(
            name='ReturnItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('count', models.FloatField(default=0, verbose_name='Количество')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('total', models.BigIntegerField(default=0, verbose_name='Сумма')),
                ('deliver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.deliver', verbose_name='Доставщик')),
                ('warehouse_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouseproduct', verbose_name='Продукт')),
            ],
        ),
    ]
