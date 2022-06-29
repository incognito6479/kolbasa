# Generated by Django 3.2.6 on 2021-12-09 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_user_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='lang',
            field=models.CharField(default='ru', max_length=255, verbose_name='Язык'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='Логин'),
        ),
    ]