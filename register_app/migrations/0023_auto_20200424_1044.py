# Generated by Django 2.2.1 on 2020-04-24 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0022_auto_20200424_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pst_filepath',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='File address'),
        ),
    ]