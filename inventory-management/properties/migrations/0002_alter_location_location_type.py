# Generated by Django 5.1.3 on 2024-12-03 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[('city', 'City')], default='city', max_length=20),
        ),
    ]
