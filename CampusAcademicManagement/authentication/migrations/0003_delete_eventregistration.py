# Generated by Django 5.1.2 on 2024-11-19 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_eventregistration'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EventRegistration',
        ),
    ]
