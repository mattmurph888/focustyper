# Generated by Django 4.2 on 2023-04-25 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0002_level_level_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_level_record',
            old_name='level_id',
            new_name='level',
        ),
        migrations.RenameField(
            model_name='user_level_record',
            old_name='user_id',
            new_name='user',
        ),
    ]
