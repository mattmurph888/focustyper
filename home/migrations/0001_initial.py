# Generated by Django 4.2 on 2023-04-25 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_title', models.CharField(max_length=50)),
                ('level_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='User_Level_Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('focus', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('level_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.level')),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
