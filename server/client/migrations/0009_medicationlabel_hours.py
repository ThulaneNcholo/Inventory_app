# Generated by Django 4.1.4 on 2023-01-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_medicationlabel'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicationlabel',
            name='Hours',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
