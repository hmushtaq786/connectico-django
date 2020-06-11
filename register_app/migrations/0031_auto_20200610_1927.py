# Generated by Django 2.2.1 on 2020-06-10 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0030_projectpostcomment_teampostcomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teampost',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='teampost',
            name='tp_id',
        ),
        migrations.AlterField(
            model_name='teampost',
            name='post_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='register_app.Post'),
        ),
    ]