# Generated by Django 2.2.1 on 2020-06-20 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0039_auto_20200620_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='t_status',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
