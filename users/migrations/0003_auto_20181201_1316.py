# Generated by Django 2.1.3 on 2018-12-01 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181126_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='correct_numbers',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='solved_numbers',
        ),
    ]