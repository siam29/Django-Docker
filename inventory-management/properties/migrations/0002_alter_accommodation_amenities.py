# Generated by Django 5.1.3 on 2024-12-04 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accommodation',
            name='amenities',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
