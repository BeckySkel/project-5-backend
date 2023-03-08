# Generated by Django 3.2.18 on 2023-03-08 22:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0010_project_contributors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(blank=True, related_name='contrib_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
