# Generated by Django 4.2.11 on 2024-04-07 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_cart', '0002_usercart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercart',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
