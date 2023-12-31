# Generated by Django 4.2.6 on 2023-11-11 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0021_alter_profilevisitedusers_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileLikeList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='liked_user', to=settings.AUTH_USER_MODEL)),
                ('visited_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
