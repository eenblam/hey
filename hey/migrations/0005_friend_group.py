# Generated by Django 4.2.2 on 2023-07-12 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hey', '0004_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hey.group'),
        ),
    ]