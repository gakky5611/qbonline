# Generated by Django 2.1.3 on 2018-11-25 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_selecthistory_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selecthistory',
            name='q_id',
        ),
    ]
