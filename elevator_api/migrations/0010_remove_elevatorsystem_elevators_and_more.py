# Generated by Django 4.2.5 on 2023-10-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_api', '0009_alter_elevatorsystem_elevators_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='elevatorsystem',
            name='elevators',
        ),
        migrations.RemoveField(
            model_name='elevatorsystem',
            name='floors',
        ),
        migrations.AddField(
            model_name='elevatorsystem',
            name='elevators',
            field=models.ManyToManyField(to='elevator_api.elevator'),
        ),
        migrations.AddField(
            model_name='elevatorsystem',
            name='floors',
            field=models.ManyToManyField(to='elevator_api.floor'),
        ),
    ]
