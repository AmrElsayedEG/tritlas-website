# Generated by Django 2.2.9 on 2020-09-22 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_auto_20200920_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='date',
            field=models.DateField(default='2020-12-30'),
        ),
    ]
