# Generated by Django 2.2.1 on 2020-06-20 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0042_task_accepted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='accepted',
            new_name='completed',
        ),
    ]
