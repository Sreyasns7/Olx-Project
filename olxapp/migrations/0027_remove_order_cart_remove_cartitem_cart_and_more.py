# Generated by Django 5.0 on 2024-02-06 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0026_order_is_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
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
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
