# Generated by Django 3.2.6 on 2022-02-28 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0026_auto_20220225_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='retailorder',
            name='comment',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='retailorder',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Время доставки'),
        ),
    ]
