# Generated by Django 4.2.11 on 2024-04-06 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='address',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='address',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
