# Generated by Django 3.2.6 on 2021-12-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter_party', '0004_auto_20211202_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='counterparty',
            name='landmark',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Оринтир'),
        ),
    ]
