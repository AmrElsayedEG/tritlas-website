# Generated by Django 2.2.9 on 2020-09-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic', '0002_auto_20200903_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('code', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='message',
            old_name='العنوان',
            new_name='البريد_الإلكتروني',
        ),
    ]
