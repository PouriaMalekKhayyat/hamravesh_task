# Generated by Django 4.1.4 on 2022-12-14 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='img_id',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
