# Generated by Django 4.1.6 on 2023-02-12 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_order_product_alter_user_phonenumber_product_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkout',
            old_name='User',
            new_name='user',
        ),
    ]
