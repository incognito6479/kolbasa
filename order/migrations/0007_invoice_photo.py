# Generated by Django 3.2.6 on 2021-12-02 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20211127_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фотография накладного'),
        ),
    ]
