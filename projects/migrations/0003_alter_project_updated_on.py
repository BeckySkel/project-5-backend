# Generated by Django 3.2.18 on 2023-02-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
