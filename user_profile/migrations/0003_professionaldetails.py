# Generated by Django 4.2.6 on 2023-10-30 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0002_rename_smoking_haibt_userbasicdetails_smoking_habit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfessionalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('education_detail', models.CharField(blank=True, max_length=255, null=True)),
                ('college', models.CharField(blank=True, max_length=255, null=True)),
                ('working_sector', models.CharField(blank=True, max_length=255, null=True)),
                ('income', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('organization', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
