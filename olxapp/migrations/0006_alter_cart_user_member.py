# Generated by Django 5.0 on 2024-02-03 03:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0005_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user_member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
