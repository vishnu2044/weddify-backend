# Generated by Django 4.2.6 on 2023-11-01 07:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReligionalPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('religion', models.CharField(max_length=100)),
                ('caste', models.CharField(max_length=100)),
                ('star', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfessionalPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('college', models.CharField(blank=True, max_length=255, null=True)),
                ('working_sector', models.CharField(blank=True, max_length=255, null=True)),
                ('income', models.CharField(blank=True, max_length=255, null=True)),
                ('occupation', models.CharField(blank=True, max_length=255, null=True)),
                ('organization', models.CharField(blank=True, max_length=255, null=True)),
                ('working_location', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BasicPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(18)])),
                ('mother_tongue', models.CharField(blank=True, max_length=100, null=True)),
                ('eating_habit', models.CharField(blank=True, max_length=100, null=True)),
                ('drinking_habit', models.CharField(blank=True, max_length=100, null=True)),
                ('smoking_habit', models.CharField(blank=True, max_length=100, null=True)),
                ('profile_created_for', models.CharField(blank=True, max_length=100, null=True)),
                ('martial_status', models.CharField(blank=True, max_length=100, null=True)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('body_type', models.CharField(blank=True, max_length=100, null=True)),
                ('physical_status', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('citizenship', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
