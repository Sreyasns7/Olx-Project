# Generated by Django 5.0 on 2024-02-04 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0013_remove_order_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
