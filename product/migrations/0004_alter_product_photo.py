# Generated by Django 3.2.6 on 2021-12-06 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='../static/crm/images/no-image.png', upload_to='product_photo', verbose_name='Фото'),
        ),
    ]