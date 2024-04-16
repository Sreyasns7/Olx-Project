# Generated by Django 5.0 on 2024-02-01 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olxapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.RemoveField(
            model_name='productsubcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='usermembers',
            name='user_member',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(default='1', max_length=10),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.DeleteModel(
            name='ProductSubcategory',
        ),
        migrations.DeleteModel(
            name='Usermembers',
        ),
    ]
