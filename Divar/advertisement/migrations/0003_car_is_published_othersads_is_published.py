# Generated by Django 5.0.6 on 2024-07-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0002_realestate_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='othersads',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]
