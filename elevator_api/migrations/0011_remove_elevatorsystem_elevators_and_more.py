# Generated by Django 4.2.5 on 2023-10-26 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elevator_api', '0010_remove_elevatorsystem_elevators_and_more'),
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
            model_name='elevator',
            name='elevator_system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elevator_api.elevatorsystem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='floor',
            name='elevator_system',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elevator_api.elevatorsystem'),
            preserve_default=False,
        ),
    ]