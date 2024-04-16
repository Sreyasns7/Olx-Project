# Generated by Django 5.0 on 2024-02-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0031_remove_cartitem_status_remove_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('unsold', 'Unsold'), ('sold', 'Sold')], default='unsold', max_length=10),
        ),
    ]
