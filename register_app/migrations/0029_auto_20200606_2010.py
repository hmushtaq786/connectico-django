# Generated by Django 2.2.1 on 2020-06-06 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register_app', '0028_auto_20200605_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectpost',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='projectpost',
            name='pp_id',
        ),
        migrations.AlterField(
            model_name='projectpost',
            name='post_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='register_app.Post'),
        ),
    ]
