# Generated by Django 4.1.6 on 2023-04-21 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Lastname',
            field=models.CharField(default=False, max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.CharField(default=False, max_length=30),
        ),
    ]
