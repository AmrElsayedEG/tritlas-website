# Generated by Django 2.2.9 on 2020-09-28 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0007_auto_20200928_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='num_of_places',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
    ]
