# Generated by Django 4.2.6 on 2023-11-10 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0015_alter_profilevisitedusers_visited_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilevisitedusers',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='profilevisitedusers',
            name='visited_profile',
        ),
        migrations.AddField(
            model_name='profilevisitedusers',
            name='visited_profile',
            field=models.ManyToManyField(null=True, related_name='visited_profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]