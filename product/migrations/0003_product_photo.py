# Generated by Django 3.2.6 on 2021-12-06 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20211122_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='../static/crm/logo.png', upload_to='product_photo', verbose_name='Фото'),
        ),
    ]
