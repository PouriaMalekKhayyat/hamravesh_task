# Generated by Django 4.1.4 on 2022-12-17 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_remove_run_img_id_run_cont_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='cont_id',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
