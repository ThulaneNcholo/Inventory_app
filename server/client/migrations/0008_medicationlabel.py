# Generated by Django 4.1.4 on 2023-01-03 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_inventorymodel_shelf'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Take', models.CharField(blank=True, max_length=200, null=True)),
                ('Times', models.CharField(blank=True, max_length=200, null=True)),
                ('ExpireDate', models.DateField(null=True)),
                ('before', models.CharField(blank=True, max_length=200, null=True)),
                ('after', models.CharField(blank=True, max_length=200, null=True)),
                ('label', models.CharField(blank=True, default='No', max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('Medication_ID', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='label_id', to='client.inventorymodel')),
            ],
        ),
    ]
