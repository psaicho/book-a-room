# Generated by Django 4.1.5 on 2023-01-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_a_room', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
