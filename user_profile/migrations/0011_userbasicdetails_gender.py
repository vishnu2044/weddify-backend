# Generated by Django 4.2.6 on 2023-11-04 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0010_country_cities'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbasicdetails',
            name='gender',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]