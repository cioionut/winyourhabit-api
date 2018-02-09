# Generated by Django 2.0.2 on 2018-02-08 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('winyourhabit_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=True)),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='negative_votes', to='winyourhabit_api.Objective')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='negative_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='negativevote',
            name='objective',
        ),
        migrations.RemoveField(
            model_name='negativevote',
            name='user',
        ),
        migrations.DeleteModel(
            name='NegativeVote',
        ),
    ]