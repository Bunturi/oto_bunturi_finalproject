# Generated by Django 5.0.6 on 2024-06-20 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_customer_old_cart_remove_customer_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]