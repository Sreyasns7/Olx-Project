# Generated by Django 5.0 on 2024-02-06 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0021_cart_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
