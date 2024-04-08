# Generated by Django 4.2.11 on 2024-04-08 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_orders_count_and_more'),
        ('order_items', '0002_remove_orderitems_master_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='orders',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.orders'),
        ),
    ]