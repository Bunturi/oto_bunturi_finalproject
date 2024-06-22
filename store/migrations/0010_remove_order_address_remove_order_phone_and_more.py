# Generated by Django 5.0.6 on 2024-06-20 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_customer_old_cart_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]