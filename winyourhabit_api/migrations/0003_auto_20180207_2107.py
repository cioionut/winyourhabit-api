# Generated by Django 2.0.2 on 2018-02-07 21:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('winyourhabit_api', '0002_auto_20180207_0719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitgroup',
            name='start_date',
        ),
        migrations.AddField(
            model_name='habitgroup',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]