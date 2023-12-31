# Generated by Django 4.2.5 on 2023-10-25 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_api', '0008_remove_elevatorsystem_elevators_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevatorsystem',
            name='elevators',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elevator_api.elevator'),
        ),
        migrations.AlterField(
            model_name='elevatorsystem',
            name='floors',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elevator_api.floor'),
        ),
    ]
