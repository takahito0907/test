# Generated by Django 3.0.3 on 2020-03-23 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0007_auto_20200324_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='photo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
