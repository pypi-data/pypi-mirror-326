# Generated by Django 3.1.2 on 2020-10-22 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djautotask', '0084_projectudftracker_taskudftracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='udf',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='udf',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
