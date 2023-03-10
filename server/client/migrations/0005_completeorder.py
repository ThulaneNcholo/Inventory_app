# Generated by Django 4.1.4 on 2022-12-27 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_medicationbasket'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quantity', models.IntegerField(blank=True, null=True)),
                ('month', models.CharField(blank=True, max_length=200, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('dateField', models.DateField(auto_now_add=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('Medication_ID', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complete', to='client.inventorymodel')),
            ],
        ),
    ]
