# Generated by Django 4.2.5 on 2023-10-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_api', '0005_elevator_door_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElevatorSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('elevators', models.ManyToManyField(to='elevator_api.elevator')),
                ('floors', models.ManyToManyField(to='elevator_api.floor')),
            ],
        ),
    ]
