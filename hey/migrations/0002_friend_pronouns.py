# Generated by Django 4.2.2 on 2023-07-13 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='pronouns',
            field=models.TextField(blank=True),
        ),
    ]