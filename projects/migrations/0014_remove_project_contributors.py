# Generated by Django 3.2.18 on 2023-03-29 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_remove_project_url_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='contributors',
        ),
    ]
