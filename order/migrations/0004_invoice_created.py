# Generated by Django 3.2.6 on 2021-11-22 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_invoice_invoiceitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]