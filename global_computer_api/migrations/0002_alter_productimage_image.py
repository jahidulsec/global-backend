# Generated by Django 4.2.7 on 2023-11-18 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_computer_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.CharField(max_length=255),
        ),
    ]