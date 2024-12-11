# Generated by Django 5.1.4 on 2024-12-11 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('Urgent', 'Urgent'), ('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=10),
        ),
    ]