# Generated by Django 3.1.1 on 2020-10-03 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djautotask', '0078_merge_20201001_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syncjob',
            name='success',
            field=models.BooleanField(null=True),
        ),
    ]
