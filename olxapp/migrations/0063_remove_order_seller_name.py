# Generated by Django 5.0 on 2024-02-27 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0062_order_seller_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='seller_name',
        ),
    ]
