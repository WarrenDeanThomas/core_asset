# Generated by Django 3.2.13 on 2022-05-30 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_core_impact'),
    ]

    operations = [
        migrations.AddField(
            model_name='corehistory',
            name='category',
            field=models.CharField(blank=True, choices=[('Maintenance', 'Maintenance'), ('Repair', 'Repair'), ('Fuel', 'Fuel'), ('Other', 'Other')], max_length=100, null=True),
        ),
    ]
