# Generated by Django 5.0 on 2024-02-29 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0087_order_seller_name_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='seller_name',
        ),
    ]
