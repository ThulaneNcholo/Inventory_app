# Generated by Django 4.1.4 on 2022-12-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_inventorymodel_medication_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorymodel',
            name='Medication_Size',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
