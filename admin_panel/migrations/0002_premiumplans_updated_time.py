# Generated by Django 4.2.6 on 2023-11-21 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='premiumplans',
            name='updated_time',
            field=models.DateField(auto_now=True),
        ),
    ]