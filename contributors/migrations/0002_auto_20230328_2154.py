# Generated by Django 3.2.18 on 2023-03-28 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0012_alter_task_options'),
        ('contributors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='creator',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='invitees', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('user', 'project', 'creator')},
        ),
    ]
