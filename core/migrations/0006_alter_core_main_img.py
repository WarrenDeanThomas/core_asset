# Generated by Django 3.2.13 on 2022-06-02 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_corehistory_km_or_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='core',
            name='main_img',
            field=models.ImageField(blank=True, default='images/avatar.png', null=True, upload_to='images/'),
        ),
    ]
