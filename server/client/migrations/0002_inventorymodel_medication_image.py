# Generated by Django 4.1.4 on 2022-12-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorymodel',
            name='Medication_Image',
            field=models.ImageField(blank=True, null=True, upload_to='files/Medication'),
        ),
    ]
