# Generated by Django 4.2.6 on 2023-10-30 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_professionaldetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionaldetails',
            name='highest_education',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
