# Generated by Django 5.0 on 2024-02-26 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0053_order_seller_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='seller_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='olxapp.product'),
        ),
    ]