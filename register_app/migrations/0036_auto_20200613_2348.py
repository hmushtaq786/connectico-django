# Generated by Django 2.2.1 on 2020-06-13 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0035_auto_20200613_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='conversation_id',
            new_name='conversation',
        ),
    ]
