# Generated by Django 5.0 on 2024-02-17 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0044_productcategory_cart_feedback_message_order_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembers',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usermembers',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
