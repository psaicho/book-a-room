# Generated by Django 4.1.5 on 2023-01-17 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_a_room', '0006_alter_roomreservation_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]