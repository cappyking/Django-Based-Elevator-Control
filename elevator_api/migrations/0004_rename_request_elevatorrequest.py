# Generated by Django 4.2.5 on 2023-10-22 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_api', '0003_request_completed'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Request',
            new_name='ElevatorRequest',
        ),
    ]