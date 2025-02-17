# Generated by Django 4.2.11 on 2024-06-11 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Kel4PSIA_web', '0014_rename_project_manager_cluster_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_location',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_type',
        ),
        migrations.AddField(
            model_name='cluster',
            name='cluster_location',
            field=models.CharField(default='', max_length=80),
        ),
        migrations.AddField(
            model_name='cluster',
            name='cluster_type',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AddField(
            model_name='sales',
            name='cluster',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='Kel4PSIA_web.cluster'),
        ),
    ]
