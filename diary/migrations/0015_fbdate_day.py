# Generated by Django 3.0.3 on 2020-03-27 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0014_fbdate_k_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbdate',
            name='day',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='day'),
        ),
    ]
