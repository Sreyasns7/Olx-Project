# Generated by Django 5.0 on 2024-02-06 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0019_remove_product_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user_member',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
