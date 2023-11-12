# Generated by Django 4.2.6 on 2023-11-01 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_preferences', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicpreferences',
            old_name='age',
            new_name='age_from',
        ),
        migrations.AddField(
            model_name='basicpreferences',
            name='age_to',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(18)]),
        ),
    ]