# Generated by Django 5.0 on 2024-02-06 03:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0020_remove_order_cart_remove_order_user_member_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('user_member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='olxapp.usermembers')),
                ('user_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='olxapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('card_number', models.CharField(max_length=16)),
                ('shipping_address', models.TextField()),
                ('cvv', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olxapp.cart')),
                ('user_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olxapp.usermembers')),
            ],
        ),
    ]