# Generated by Django 4.2.5 on 2023-09-14 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_charcode_currency_char_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Currency',
        ),
    ]
