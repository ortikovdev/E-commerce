# Generated by Django 4.2.11 on 2024-05-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]