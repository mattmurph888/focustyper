# Generated by Django 4.2 on 2023-04-25 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='level_number',
            field=models.IntegerField(default=None, unique=True),
        ),
    ]
