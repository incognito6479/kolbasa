# Generated by Django 3.2.6 on 2021-12-10 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counter_party', '0011_auto_20211210_2020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='name',
            new_name='full_name',
        ),
    ]
